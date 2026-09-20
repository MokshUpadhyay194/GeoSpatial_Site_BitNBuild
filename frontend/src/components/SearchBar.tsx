import React, { useState, useEffect, useRef, useMemo, useCallback } from "react";
import {
  Search, MapPin, X, Loader2, Navigation,
  Building2, Factory, Landmark, Compass,
} from "lucide-react";

export interface SearchResultItem {
  id: string;
  name: string;
  subTitle: string;
  lat: number;
  lng: number;
  category: "benchmark" | "ward" | "city" | "industrial" | "geocoded" | "coordinate";
  district?: string;
  icon?: React.ComponentType<{ className?: string }>;
}

import { COMPREHENSIVE_PRESETS } from "@/data/nationalGazetteerPresets";

const LOCAL_FALLBACK_PRESETS: SearchResultItem[] = COMPREHENSIVE_PRESETS;

function getCategoryIcon(category?: string): React.ComponentType<{ className?: string }> {
  switch (category) {
    case "benchmark": return Building2;
    case "coordinate": return Compass;
    case "industrial": return Factory;
    case "city": return Landmark;
    case "geocoded": return Navigation;
    default: return MapPin;
  }
}

interface SearchBarProps {
  currentAddress?: string;
  onSelectLocation: (result: { name: string; lat: number; lng: number; category?: string; subTitle?: string }) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ currentAddress = "SG Highway, Bodakdev, Ahmedabad", onSelectLocation }) => {
  const [query, setQuery] = useState(currentAddress);
  const [isOpen, setIsOpen] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<SearchResultItem[]>(LOCAL_FALLBACK_PRESETS.slice(0, 6));
  const [selectedIndex, setSelectedIndex] = useState<number>(-1);

  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  useEffect(() => {
    if (currentAddress && currentAddress !== query) setQuery(currentAddress);
  }, [currentAddress]);

  const coordinateMatch = useMemo(() => {
    const trimmed = query.trim();
    const m = trimmed.match(/^([-+]?\d{1,2}(?:\.\d+)?)[,\s]+([-+]?\d{1,3}(?:\.\d+)?)$/);
    if (m) {
      const lat = parseFloat(m[1]);
      const lng = parseFloat(m[2]);
      if (!isNaN(lat) && !isNaN(lng) && lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) return { lat, lng };
    }
    return null;
  }, [query]);

  const fetchSearchResults = useCallback(async (searchQuery: string) => {
    if (abortControllerRef.current) abortControllerRef.current.abort();
    const controller = new AbortController();
    abortControllerRef.current = controller;

    const qLower = searchQuery.toLowerCase().trim();
    if (!qLower) {
      setSearchResults(LOCAL_FALLBACK_PRESETS.slice(0, 6));
      setIsSearching(false);
      return;
    }

    // 1. Instant local match across name, subtitle, and district
    const localFiltered = LOCAL_FALLBACK_PRESETS.filter(
      (p) =>
        p.name.toLowerCase().includes(qLower) ||
        p.subTitle.toLowerCase().includes(qLower) ||
        (p.district && p.district.toLowerCase().includes(qLower))
    );

    // Immediately show local matches while fetching backend geocoder
    if (localFiltered.length > 0) {
      setSearchResults(localFiltered);
    }

    setIsSearching(true);

    try {
      // 2. Fetch from backend /api/search (curated places + live geocoding)
      const resp = await fetch("/api/search?q=" + encodeURIComponent(searchQuery) + "&limit=8", {
        signal: controller.signal,
      });

      if (resp.ok) {
        const data = await resp.json();
        if (data.results && Array.isArray(data.results) && data.results.length > 0) {
          const backendItems: SearchResultItem[] = data.results.map((r: any) => ({
            id: r.id || `res-${r.lat}-${r.lng}`,
            name: r.name,
            subTitle: r.subTitle || `${r.district || "Location"} (${r.lat.toFixed(4)}, ${r.lng.toFixed(4)})`,
            lat: r.lat,
            lng: r.lng,
            category: r.category || "city",
            district: r.district,
            icon: getCategoryIcon(r.category),
          }));

          // Merge local and backend items deduplicated by proximity (~500m)
          const merged: SearchResultItem[] = [...backendItems];
          localFiltered.forEach((loc) => {
            if (!merged.some((m) => Math.abs(m.lat - loc.lat) < 0.005 && Math.abs(m.lng - loc.lng) < 0.005)) {
              merged.push(loc);
            }
          });

          setSearchResults(merged.slice(0, 8));
          setIsSearching(false);
          return merged;
        }
      }

      // If backend returned 0 results, keep whatever local presets matched (or empty)
      setSearchResults(localFiltered);
    } catch (err: any) {
      if (err.name !== "AbortError") {
        setSearchResults(localFiltered);
      }
    } finally {
      setIsSearching(false);
    }
  }, []);

  useEffect(() => {
    const q = query.trim();
    if (!q) {
      setSearchResults(LOCAL_FALLBACK_PRESETS.slice(0, 6));
      return;
    }
    const timer = setTimeout(() => fetchSearchResults(q), 250);
    return () => clearTimeout(timer);
  }, [query, fetchSearchResults]);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSelect = (item: SearchResultItem) => {
    setQuery(item.name);
    setIsOpen(false);
    onSelectLocation({
      name: item.name,
      lat: item.lat,
      lng: item.lng,
      category: item.category,
      subTitle: item.subTitle,
    });
  };

  const handleExecuteSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();

    // 1. Direct coordinate entry
    if (coordinateMatch) {
      handleSelect({
        id: "coord-custom",
        name: `Coordinates: ${coordinateMatch.lat.toFixed(4)}° N, ${coordinateMatch.lng.toFixed(4)}° E`,
        subTitle: "Direct GPS Coordinates",
        lat: coordinateMatch.lat,
        lng: coordinateMatch.lng,
        category: "coordinate",
        icon: Compass,
      });
      return;
    }

    // 2. Currently highlighted item
    if (selectedIndex >= 0 && selectedIndex < searchResults.length) {
      handleSelect(searchResults[selectedIndex]);
      return;
    }

    // 3. Top match in current list
    if (searchResults.length > 0) {
      handleSelect(searchResults[0]);
      return;
    }

    // 4. Fallback live fetch if list was empty
    const q = query.trim();
    if (!q) return;

    setIsSearching(true);
    try {
      const resp = await fetch("/api/search?q=" + encodeURIComponent(q) + "&limit=4");
      if (resp.ok) {
        const data = await resp.json();
        if (data.results && data.results.length > 0) {
          const top = data.results[0];
          handleSelect({
            id: top.id,
            name: top.name,
            subTitle: top.subTitle,
            lat: top.lat,
            lng: top.lng,
            category: top.category,
            district: top.district,
            icon: getCategoryIcon(top.category),
          });
        }
      }
    } catch {
      /* ignore */
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setIsOpen(true);
      setSelectedIndex((prev) => (prev < searchResults.length - 1 ? prev + 1 : 0));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : searchResults.length - 1));
    } else if (e.key === "Enter") {
      e.preventDefault();
      handleExecuteSearch();
    } else if (e.key === "Escape") {
      setIsOpen(false);
    }
  };

  const handleClear = () => {
    setQuery("");
    setIsOpen(true);
    setSearchResults(LOCAL_FALLBACK_PRESETS.slice(0, 6));
    inputRef.current?.focus();
  };

  const hasNoResults = isOpen && !isSearching && searchResults.length === 0 && query.trim().length > 0;

  return (
    <div ref={containerRef} className="relative w-full">
      <form
        onSubmit={handleExecuteSearch}
        className="h-10 bg-surface border border-slate-200 dark:border-slate-700 rounded-panel shadow-float px-3 flex items-center gap-2 transition-all focus-within:ring-2 focus-within:ring-brand-600/40 focus-within:border-brand-600"
      >
        <Search className="w-4 h-4 text-slate-500 shrink-0" strokeWidth={1.75} />
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
            setSelectedIndex(-1);
          }}
          onFocus={() => setIsOpen(true)}
          onKeyDown={handleKeyDown}
          placeholder="Search any Gujarat city, ward, or address (e.g. Vadodara, Surat, Bhavnagar, 22.31 73.18)"
          className="w-full bg-transparent text-xs text-ink placeholder:text-slate-500 outline-none"
        />
        {isSearching && <Loader2 className="w-3.5 h-3.5 text-brand-600 animate-spin shrink-0" />}
        {query && !isSearching && (
          <button
            type="button"
            onClick={handleClear}
            className="p-1 text-slate-400 hover:text-ink transition-colors shrink-0"
            title="Clear search"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
        <button
          type="submit"
          className="h-7 px-3 bg-brand-600 hover:bg-brand-700 active:scale-95 text-surface text-xs font-semibold rounded-chip flex items-center gap-1.5 transition-all shadow-xs shrink-0 cursor-pointer select-none"
          title="Search this location"
        >
          <Search className="w-3.5 h-3.5" strokeWidth={2} />
          <span>Search</span>
        </button>
      </form>

      {/* Dropdown Results */}
      {isOpen && (searchResults.length > 0 || hasNoResults || coordinateMatch) && (
        <div className="absolute left-0 right-0 top-11 mt-1 bg-surface/95 dark:bg-slate-900/95 backdrop-blur-md border border-slate-200 dark:border-slate-800 rounded-panel shadow-2xl z-50 max-h-[380px] overflow-y-auto divide-y divide-slate-100 dark:divide-slate-800/60 animate-in fade-in slide-in-from-top-1 duration-150">
          {/* Coordinates Quick Jumper */}
          {coordinateMatch && (
            <div
              onClick={() =>
                handleSelect({
                  id: "coord-custom",
                  name: `Coordinates: ${coordinateMatch.lat.toFixed(4)}° N, ${coordinateMatch.lng.toFixed(4)}° E`,
                  subTitle: "Direct GPS Coordinates",
                  lat: coordinateMatch.lat,
                  lng: coordinateMatch.lng,
                  category: "coordinate",
                  icon: Compass,
                })
              }
              className="p-2.5 bg-brand-50/80 dark:bg-brand-950/40 border-b border-brand-100 dark:border-brand-900/50 flex items-center justify-between cursor-pointer hover:bg-brand-100/70 transition-colors"
            >
              <div className="flex items-center gap-2">
                <Compass className="w-4 h-4 text-brand-600 dark:text-brand-400" />
                <div>
                  <span className="text-xs font-medium text-brand-900 dark:text-brand-200">
                    Jump to Coordinates: {coordinateMatch.lat.toFixed(4)}, {coordinateMatch.lng.toFixed(4)}
                  </span>
                  <p className="text-[10px] text-slate-500">Press Enter or click to evaluate site</p>
                </div>
              </div>
              <span className="text-[10px] bg-brand-600 text-white px-2 py-0.5 rounded font-mono font-medium">
                Enter
              </span>
            </div>
          )}

          {/* Empty Search State */}
          {hasNoResults && !coordinateMatch && (
            <div className="p-4 text-center text-xs text-slate-500 flex flex-col items-center gap-1.5">
              <MapPin className="w-5 h-5 text-slate-400" />
              <p className="font-medium text-ink">No locations matching "{query}"</p>
              <p className="text-[11px] text-slate-400">
                Press <span className="font-mono px-1 py-0.5 bg-slate-100 dark:bg-slate-800 rounded">Enter</span> or click Search to query worldwide geocoding.
              </p>
            </div>
          )}

          {/* List of matched items */}
          {searchResults.length > 0 && (
            <div className="py-1">
              {searchResults.map((item, idx) => {
                const Icon = item.icon || MapPin;
                const isSelected = idx === selectedIndex;
                return (
                  <button
                    type="button"
                    key={item.id}
                    onClick={() => handleSelect(item)}
                    onMouseEnter={() => setSelectedIndex(idx)}
                    className={`w-full text-left px-3 py-2 flex items-start gap-2.5 transition-colors ${
                      isSelected
                        ? "bg-brand-50/80 dark:bg-brand-950/50 text-brand-900 dark:text-brand-200"
                        : "hover:bg-slate-100/70 dark:hover:bg-slate-800/60 text-ink"
                    }`}
                  >
                    <div
                      className={`mt-0.5 w-6 h-6 rounded-md flex items-center justify-center shrink-0 ${
                        item.category === "benchmark"
                          ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
                          : item.category === "coordinate"
                          ? "bg-blue-500/10 text-blue-600 dark:text-blue-400"
                          : item.category === "industrial"
                          ? "bg-amber-500/10 text-amber-600 dark:text-amber-400"
                          : item.category === "geocoded"
                          ? "bg-sky-500/10 text-sky-600 dark:text-sky-400"
                          : "bg-slate-200/50 dark:bg-slate-800 text-slate-600 dark:text-slate-400"
                      }`}
                    >
                      <Icon className="w-3.5 h-3.5" strokeWidth={2} />
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-2">
                        <span className="text-xs font-medium truncate">{item.name}</span>
                        <span
                          className={`text-[10px] uppercase tracking-wider px-1.5 rounded font-mono font-medium shrink-0 ${
                            item.category === "benchmark"
                              ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950/80 dark:text-emerald-300"
                              : item.category === "coordinate"
                              ? "bg-blue-100 text-blue-800 dark:bg-blue-950/80 dark:text-blue-300"
                              : item.category === "industrial"
                              ? "bg-amber-100 text-amber-800 dark:bg-amber-950/80 dark:text-amber-300"
                              : item.category === "geocoded"
                              ? "bg-sky-100 text-sky-800 dark:bg-sky-950/80 dark:text-sky-300"
                              : "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400"
                          }`}
                        >
                          {item.category === "geocoded" ? "OSM" : item.category}
                        </span>
                      </div>

                      <p className="text-[11px] text-slate-500 truncate mt-0.5">{item.subTitle}</p>
                      <div className="text-[10px] font-mono text-slate-400 mt-0.5">
                        {item.lat.toFixed(4)}° N, {item.lng.toFixed(4)}° E
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          )}

          {/* Dropdown Footer */}
          <div className="px-3 py-1.5 bg-canvas/60 dark:bg-slate-900/60 flex items-center justify-between text-[10px] text-slate-500">
            <span>
              {searchResults.length} location{searchResults.length !== 1 ? "s" : ""} found
            </span>
            <div className="flex items-center gap-2">
              <span>↑↓ Navigate</span>
              <span>↵ Select</span>
              <span>Esc Close</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
