# Icon Library · Inline SVG Replacements for Every Emoji

Every emoji in a deck becomes an inline SVG line icon. Same stroke weight across a deck (1.8 or 2.0 usually; 2.4 for enterprise feel). Same color as the surrounding text by default (use `currentColor`), accented with brand primary where emphasis is needed.

All icons use:
- `viewBox="0 0 24 24"` (the universal icon viewBox)
- `fill="none"`
- `stroke="currentColor"`
- `stroke-width="2"` (adjust 1.8 to 2.4 per brand weight)
- `stroke-linecap="round"`
- `stroke-linejoin="round"`

Render each icon at the size you need (typically 16px, 20px, or 28px).

---

## Navigation / controls

**Chevron left (prev)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
```

**Chevron right (next)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>
```

**X / close**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6L6 18M6 6l12 12"/></svg>
```

---

## Status / confirmation

**Checkmark (success)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
```

**Circle-check (success pill)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 12l3 3 5-6"/></svg>
```

**Info**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
```

**Warning / alert**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.8L1.8 18a2 2 0 001.7 3h16.9a2 2 0 001.7-3L13.7 3.8a2 2 0 00-3.4 0zM12 9v4M12 17h.01"/></svg>
```

---

## Affection / rating

**Heart (outline)** · save for listing favorites
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.8 4.6a5.5 5.5 0 00-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 00-7.8 7.8l1 1.1L12 21l7.8-7.8 1-1.1a5.5 5.5 0 000-7.8z"/></svg>
```

**Heart (filled)** · for "liked" state
```svg
<svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M20.8 4.6a5.5 5.5 0 00-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 00-7.8 7.8l1 1.1L12 21l7.8-7.8 1-1.1a5.5 5.5 0 000-7.8z"/></svg>
```

**Star (filled)** · for rating
```svg
<svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 17.3l-6.2 3.7 1.7-7-5.4-4.7 7.1-.6L12 2l2.8 6.7 7.1.6-5.4 4.7 1.7 7z"/></svg>
```

---

## Problem / solution cards (Airbnb pattern)

**Dollar sign (cost / pricing)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
```

**Building (hotel / corporate)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22V12h6v10M9 6h.01M15 6h.01M9 10h.01M15 10h.01"/></svg>
```

**House (home / property)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12l9-9 9 9M5 10v10h14V10"/></svg>
```

**Users / community**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M9 11a4 4 0 100-8 4 4 0 000 8zM23 21v-2a4 4 0 00-3-3.9M16 3.1a4 4 0 010 7.8"/></svg>
```

---

## GTM motions

**Megaphone (marketing)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11v3a4 4 0 004 4h2l7 5V5L9 10H7a4 4 0 00-4 1z"/></svg>
```

**Arrow trend up (growth)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
```

**Connecting arrows (partnerships)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 014-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 01-4 4H3"/></svg>
```

**Camera (content / brand)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/><circle cx="12" cy="13" r="4"/></svg>
```

**Document (content / press)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>
```

---

## Amenities (Airbnb-style feature lists)

**Wi-Fi**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13a10 10 0 0114 0M8.5 16.5a5 5 0 017 0M2 8.8a15 15 0 0120 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>
```

**Kitchen (utensils)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v6a2 2 0 002 2h2v12M7 2v8M21 15V2a5 5 0 00-5 5v6a2 2 0 002 2h3zm0 0v7"/></svg>
```

**Washer (laundry)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="12" cy="14" r="4"/><path d="M7 7h.01M11 7h.01"/></svg>
```

**AC / climate**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h20M12 2v20M5 5l14 14M19 5L5 19"/></svg>
```

**Elevator**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="1"/><path d="M12 6l-2 2 2 2M12 14l2 2-2 2"/></svg>
```

---

## Product / tech

**Lightning bolt (speed / power)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10"/></svg>
```

**Lock (security)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
```

**Sparkles (AI / magic)**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2 5 5 2-5 2-2 5-2-5-5-2 5-2zM19 15l1 2 2 1-2 1-1 2-1-2-2-1 2-1zM5 6l1 2 2 1-2 1-1 2-1-2-2-1 2-1z"/></svg>
```

**Database**
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
```

---

## Extending the library

When a new template needs an icon not in this set:

1. Keep the viewBox at `24x24`, stroke at 2 (adjust to brand weight), linecap/linejoin round
2. Match the geometric abstraction level. These are Feather-style simple line icons, not detailed illustrations
3. Add the new icon to this file with a short label
4. Reuse across templates wherever possible so the visual language stays consistent

Never drop an emoji in because "it's faster." Every emoji breaks the brand-accurate illusion.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
