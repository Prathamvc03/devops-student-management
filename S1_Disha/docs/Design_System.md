# EduTrack — UI/UX Design System

This document outlines the official design tokens, typography, and component guidelines implemented in the Student Management System. This ensures consistent, accessible, and inclusive design standards.

## 1. Design Tokens & Color Palette

We utilize a modern SaaS color palette optimized for accessibility (WCAG AA contrast) and an authoritative, clean academic aesthetic.

### Brand Colors (Indigo Palette)
The primary brand communicates academic integrity, authority, and professionalism.
- **Brand Primary:** `#4f46e5` (Tailwind `indigo-600`) — Primary buttons, active tabs, and primary actions.
- **Brand Hover:** `#4338ca` (Tailwind `indigo-700`) — Interaction feedback and hover states.
- **Brand Light:** `#e0e7ff` (Tailwind `indigo-100`) — Soft accent backgrounds, active badges.

### Status Colors
- **Active / Enrolled:** `#059669` (Tailwind `emerald-600`) / Background: `#ecfdf5`
- **Pending Review:** `#d97706` (Tailwind `amber-600`) / Background: `#fef3c7`
- **Graduated / Inactive:** `#475569` (Tailwind `slate-600`) / Background: `#f1f5f9`
- **Rejected / Error:** `#e11d48` (Tailwind `rose-600`) / Background: `#ffe4e6`

### Interface Neutral Colors (Slate)
Slate provides cool, crisp contrast reducing eye strain compared to harsh black and white.
- **Background:** `#f8fafc` (Tailwind `slate-50`)
- **Card Background:** `#ffffff` (White)
- **Primary Text:** `#0f172a` (Tailwind `slate-900`) — High contrast headings and titles.
- **Body Text:** `#334155` (Tailwind `slate-700`) — High legibility body text.
- **Secondary Text:** `#64748b` (Tailwind `slate-500`) — Metadata, dates, IDs.
- **Borders/Dividers:** `#e2e8f0` (Tailwind `slate-200`)

---

## 2. Typography

To give the application a modern, university-grade feel, we implement **Plus Jakarta Sans** and **Inter**.

- **Font Family:** `'Plus Jakarta Sans', 'Inter', system-ui, sans-serif`
- **Headings (h1):** `font-extrabold`, `text-2xl` to `text-3xl`, tracking tight (`tracking-tight`).
- **Section Headings (h2, h3):** `font-bold`, `text-base` to `text-lg`.
- **Body Text:** `font-normal`, `text-sm`, line-height `relaxed`.
- **Badges / Meta:** `font-semibold`, `text-xs`, uppercase or title case.

---

## 3. UI Component Architecture

### The Student Profile Card
The primary interactive component of the public student directory.
- **Information Hierarchy:**
  1. Student Avatar initials & Name (Bold, high contrast)
  2. Student ID badge (Mono font, subdued)
  3. Status Badge (Top right, color-coded)
  4. Department & Course Program (Subdued metadata chip)
  5. Academic Year (Clear progress indicator)
  6. Action Link ("View Profile &rarr;")
- **Shadows:** `shadow-xs` resting state, transitioning to `shadow-md` and border highlight on hover.

### Accessibility (A11y) & Inclusivity
- **Zero Emojis Policy:** Decorative emojis are strictly prohibited in code and UI templates. Clean, semantic SVG icons equipped with `aria-hidden="true"` are used exclusively.
- **Color Independence:** Statuses like "Enrolled" and "Pending" rely on both text and color, ensuring color-blind users can navigate the system easily.
- **Focus States:** All interactive elements (`<button>`, `<a>`, `<input>`, `<select>`) have clear focus rings for keyboard navigators.

---

## 4. Animation & Micro-Interactions
- **Modal Transitions:** Spring-like modal fade-in (`scale(0.96) translateY(8px)` &rarr; `scale(1) translateY(0)` in 0.25s).
- **Toasts:** Bottom-right slide-and-fade toasts for instant non-blocking user feedback.
- **Loading Spinners:** Minimal CSS spinners embedded in submit buttons during async HTTP operations.
