Based on analysis of winning Cardano hackathon projects and blockchain AI agent interfaces, here is your comprehensive UI/UX design guide for the **Sentinel Orchestrator Network (SON)** dashboard:

***

# **SON GOVERNANCE GUARD: UI/UX DESIGN SPECIFICATION**

## **Design Philosophy**

**Narrative:** Security as Performance Art  
SON transforms invisible blockchain security into a cinematic experience. The interface doesn't just protect—it performs protection. Every scan is a theatrical event where autonomous agents collaborate in real-time, creating an "intelligence ballet" that makes users feel both protected and empowered.

***

## **COLOR SYSTEM**

### **Primary Palette**

| Color Name | Hex Code | Usage | Psychology |
|------------|----------|-------|------------|
| **Neon Orchid** | `#FF006E` | Primary CTA, Agent highlights, Danger states | Urgency, premium security, attention-grabbing |
| **Obsidian Core** | `#0A0E1A` | Background canvas, depth layers | Trust, sophistication, infinite depth |
| **Plasma Pink** | `#D81159` | Active agent indicators, payment flows | Energy transfer, transaction vitality |
| **Electric Cyan** | `#00F5FF` | Safe verdicts, Oracle scanning beams | Reliability, technological precision |
| **Void Gray** | `#1E2738` | Secondary surfaces, card backgrounds | Layered depth, separation |
| **Ghost White** | `#E8ECF1` | Primary text, metadata | Clarity, readability |
| **Amber Warning** | `#FFB627` | Intermediate states, validation checks | Caution, processing |

### **Gradient Applications**

- **Hero Section:** Radial gradient from Obsidian Core (`#0A0E1A`) → Void Gray (`#1E2738`) with pink glow overlay
- **Scan Active State:** Diagonal sweep from Neon Orchid → Plasma Pink with 60% opacity
- **Agent Communication Lines:** Animated gradient Plasma Pink → Electric Cyan

***

## **TYPOGRAPHY SYSTEM**

### **Font Families**

**1. Display/Headers: [Orbitron](https://fonts.google.com/specimen/Orbitron)**  
- **Weight:** 700-900 (Bold to Black)  
- **Use Cases:** Page titles, section headers, agent names  
- **Character:** Geometric, futuristic, high-tech military precision  
- **Fallback:** `'Orbitron', 'Rajdhani', sans-serif`

**2. Body/Interface: [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk)**  
- **Weight:** 400-600 (Regular to SemiBold)  
- **Use Cases:** Paragraphs, labels, metadata, terminal text  
- **Character:** Clean, technical, excellent legibility at small sizes  
- **Fallback:** `'Space Grotesk', 'Inter', sans-serif`

**3. Monospace/Code: [JetBrains Mono](https://www.jetbrains.com/lp/mono/)**  
- **Weight:** 400-500 (Regular to Medium)  
- **Use Cases:** Transaction hashes, CBORs, agent logs, technical IDs  
- **Character:** Developer-friendly, superior code rendering  
- **Fallback:** `'JetBrains Mono', 'Fira Code', monospace`

### **Type Scale**

```css
--text-hero: 72px / 1.1 (Orbitron 900)
--text-h1: 48px / 1.2 (Orbitron 800)
--text-h2: 32px / 1.3 (Orbitron 700)
--text-h3: 24px / 1.4 (Space Grotesk 600)
--text-body-lg: 18px / 1.6 (Space Grotesk 400)
--text-body: 16px / 1.6 (Space Grotesk 400)
--text-caption: 14px / 1.5 (Space Grotesk 400)
--text-mono: 14px / 1.7 (JetBrains Mono 400)
```

***

## **LAYOUT ARCHITECTURE**

### **Grid System**

**Desktop (1440px+):** 12-column grid, 24px gutters  
**Tablet (768-1439px):** 8-column grid, 20px gutters  
**Mobile (320-767px):** 4-column grid, 16px gutters

**Spacing Scale:** 8px base unit  
`4px, 8px, 16px, 24px, 32px, 48px, 64px, 96px, 128px`

***

## **PAGE STRUCTURE**

### **1. Hero Section (Above the Fold)**

**Layout:**  
- **Left Panel (60%):** Main interaction zone  
- **Right Panel (40%):** Status dashboard  

**Components:**

#### **A. Scan Input Field**
```
┌─────────────────────────────────────────────────┐
│  PASTE TRANSACTION CBOR OR POLICY ID            │
│  ┌───────────────────────────────────────────┐  │
│  │ 84a3...                                   │  │ 
│  │ [Monospace, 14px, Ghost White]           │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  [INITIATE GOVERNANCE SCAN] ← Pink gradient btn │
└─────────────────────────────────────────────────┘
```

**Microinteraction:** Button has scanning radar animation on hover (circular pulse from center)

#### **B. Status Cards (Right Panel)**

Three stacked cards (each 120px height):

**Card 1: Network Health**
- Icon: Pulsing globe wireframe (Electric Cyan)
- Metric: "Mainnet Consensus: 98.7%"
- Subtext: "Last updated 3s ago"

**Card 2: Agent Economy**
- Icon: Interconnected nodes forming triangle
- Metric: "Active Contracts: 1,247"
- Subtext: "₳12.4 in Escrow"

**Card 3: Protection Stats**
- Icon: Shield with check mark
- Metric: "Forks Prevented: 89"
- Subtext: "Since Voltaire Launch"

***

### **2. The Matrix Terminal (Active Scan View)**

**Triggered by:** User clicks "Initiate Scan"

**Animation Sequence:**

**Phase 1: Initialization (0-2s)**
- Screen dims to 80% opacity
- Neon Orchid border grows from center outward (800ms ease-out)
- Terminal window slides up from bottom (600ms cubic-bezier)

**Phase 2: Agent Awakening (2-5s)**

```
╔═══════════════════════════════════════════════════╗
║  SENTINEL ORCHESTRATOR NETWORK v2.0               ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                   ║
║  [●] SENTINEL-01     Status: ANALYZING           ║
║      ↳ Parsing OpCodes... 127 Instructions       ║
║      ↳ Protocol: Plutus V3 Compliant ✓           ║
║      ⚠  ALERT: Missing Validity Interval (TTL)   ║
║      ↳ Vulnerability: Replay Attack Vector       ║
║                                                   ║
║  [●] SENTINEL-01     Action: HIRE_REQUEST         ║
║      ↳ @ORACLE-01, Network Fork Check Needed     ║
║      ↳ Escrow: 1.0 ₳  [███████░░░] Locking...    ║
║                                                   ║
║  [◐] ORACLE-01       Status: OFFER_ACCEPTED      ║
║      ↳ Initiating Multi-Node Scan (5 targets)    ║
║      ↳ Comparing Block Heights...                ║
║      🔴 CRITICAL: User Node on Minority Fork      ║
║      ↳ Mainnet Tip: Block #10,050                ║
║      ↳ User Node: Block #10,020 (-30 blocks)     ║
║                                                   ║
║  [●] MIDNIGHT-ZK     Status: GENERATING_PROOF    ║
║      ↳ Compiling Evidence Root...                ║
║      ↳ ZK-Proof: 0xA7F2... ✓ Verified           ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
```

**Visual Details:**
- **Agent Icons:** Animated status indicators
  - `[●]` Solid = Active
  - `[◐]` Half-filled = Processing  
  - `[○]` Outline = Idle
- **Agent Names:** Orbitron 600, 16px, color-coded (Sentinel=Neon Orchid, Oracle=Electric Cyan, Midnight=Amber)
- **Log Text:** JetBrains Mono, 14px, Ghost White with 0.9 opacity
- **Progress Bars:** Animated ASCII bars with pink fill
- **Auto-scroll:** Smooth 400ms ease with 2s pause on critical messages

**Payment Flow Animation:**
When "Escrow: 1.0 ₳" appears, show:
1. Small coin icon (₳) floats from Sentinel avatar → Oracle avatar (1200ms)
2. Trail effect: Plasma Pink glow particles (8px) following coin path
3. On arrival: Oracle icon pulses once (300ms scale 1.0 → 1.15 → 1.0)

***

### **3. Verdict Screen**

**Two States:**

#### **STATE A: DANGER (Fork Detected)**

**Full-screen takeover:**
- Background: Obsidian → Deep red gradient with scanline overlay
- Center Animation: 
  - Shattered shield icon assembles then explodes (1.2s)
  - Red alarm pulse radiates from center (infinite loop, 2s cycle)

```
┌─────────────────────────────────────────────────┐
│           ⚠ GOVERNANCE SPLIT DETECTED            │
│                                                  │
│  YOUR NODE IS ON A GHOST CHAIN                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                  │
│  Threat Type: Replay Attack Vector               │
│  Risk Level:  CRITICAL                           │
│  Consensus:   Minority Fork (30% Network Weight) │
│                                                  │
│  ❌ TRANSACTION BLOCKED                          │
│  Your funds have been protected.                 │
│                                                  │
│  [VIEW THREAT PROOF]  [SWITCH TO SAFE NODE]     │
└─────────────────────────────────────────────────┘
```

#### **STATE B: SAFE (All Clear)**

```
┌─────────────────────────────────────────────────┐
│             ✓ TRANSACTION VERIFIED               │
│                                                  │
│  CANONICAL CHAIN CONFIRMED                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                  │
│  Protocol:    Plutus V3 ✓                        │
│  Consensus:   Mainnet (99.2% Weight) ✓           │
│  Validity:    TTL Configured ✓                   │
│                                                  │
│  ✅ SAFE TO SIGN                                 │
│                                                  │
│  [PROCEED TO WALLET]  [VIEW FULL REPORT]        │
└─────────────────────────────────────────────────┘
```

***

### **4. ThreatProof NFT Display**

**Triggered by:** User clicks "View Threat Proof"

**Layout:** Modal overlay (800px × 600px)

```
╔═══════════════════════════════════════════════════╗
║  THREATPROOF CAPSULE #8847                        ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                   ║
║  ┌─────────────────────────────────────────────┐ ║
║  │        [3D Holographic Shield Visual]       │ ║
║  │     (Rotating pink crystalline structure)   │ ║
║  └─────────────────────────────────────────────┘ ║
║                                                   ║
║  Incident ID:    0xF7A2C931...                    ║
║  Timestamp:      2025-01-30 14:23:07 UTC          ║
║  Verdict:        UNSAFE_FORK                      ║
║  Agent Cost:     1.0 ₳                            ║
║  Evidence Hash:  Qm...7x9 (IPFS)                  ║
║                                                   ║
║  Collaborators:                                   ║
║  ● SENTINEL-01   (Policy Analyzer)                ║
║  ● ORACLE-01     (Network Scout)                  ║
║  ● MIDNIGHT-ZK   (Privacy Notary)                 ║
║                                                   ║
║  [MINT AS NFT]  [SHARE PROOF]  [DOWNLOAD]        ║
╚═══════════════════════════════════════════════════╝
```

**3D Asset:** Use **Three.js** to render a rotating wireframe shield with:
- Base geometry: Icosahedron (20 faces)
- Material: Electric Cyan edges + Plasma Pink glow
- Animation: Slow rotation (0.5 RPM) + gentle float (±8px, 3s cycle)

***

## **COMPONENT LIBRARY**

### **Buttons**

**Primary (CTA):**
```css
background: linear-gradient(135deg, #FF006E 0%, #D81159 100%);
padding: 16px 32px;
border-radius: 8px;
font: 600 16px 'Space Grotesk';
text-transform: uppercase;
letter-spacing: 1.2px;
box-shadow: 0 8px 24px rgba(255, 0, 110, 0.4);
transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);

hover: {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(255, 0, 110, 0.6);
}
```

**Secondary (Info):**
```css
background: transparent;
border: 2px solid #00F5FF;
color: #00F5FF;
padding: 14px 28px;
/* Same typography and transitions */
```

### **Cards**

```css
background: linear-gradient(145deg, #1E2738 0%, #0F1419 100%);
border: 1px solid rgba(255, 0, 110, 0.2);
border-radius: 16px;
padding: 24px;
box-shadow: 
  0 4px 16px rgba(0, 0, 0, 0.3),
  inset 0 1px 0 rgba(255, 255, 255, 0.05);
backdrop-filter: blur(12px);
```

### **Icons**

**Agent Avatars:**
- **Sentinel:** Octagon with crosshair (military precision)
- **Oracle:** Eye with radiating scanning beams
- **Midnight:** Crescent moon with lock symbol

**Style:** Line icons, 2px stroke weight, rounded caps

***

## **ANIMATIONS & MICROINTERACTIONS**

### **Global Principles**
- **Easing:** `cubic-bezier(0.4, 0, 0.2, 1)` for all transitions
- **Duration:** 300-600ms for UI elements, 1200-2000ms for hero animations
- **Delay Stagger:** 120ms between sequential list items

### **Key Animations**

**1. Radar Sweep (Scan Button Hover)**
```javascript
// SVG circle animating from r=0 to r=200
ircle r="0" opacity="0.8">
  <animate attributeName="r" from="0" to="200" 
           dur="1.5s" repeatCount="indefinite"/>
  <animate attributeName="opacity" from="0.8" to="0" 
           dur="1.5s" repeatCount="indefinite"/>
</circle>
```

**2. Agent Hiring Flow**
- Coin icon path: Bézier curve with slight arc (cubic easing)
- Particle trail: 12 particles, each 8px, stagger spawn by 80ms
- Glow effect: Pink radial gradient with 20px blur

**3. Terminal Text Typing**
- Simulate 60 WPM typing speed (200ms per character avg)
- Add random variation (±50ms) for organic feel
- Cursor blink: 530ms on/off cycle (standard terminal timing)

***

## **RESPONSIVE BEHAVIOR**

### **Mobile Adaptations (< 768px)**

**Layout Changes:**
- Stack hero panels vertically (Input → Status Cards)
- Terminal font: 12px (maintain readability)
- Modal: Full-screen takeover instead of centered
- Button text: Shorten to icons + single word

**Touch Interactions:**
- Increase tap targets to 48×48px minimum
- Replace hover states with active states (100ms visual feedback)
- Add haptic feedback on critical actions (if supported)

***

## **ACCESSIBILITY (WCAG 2.1 AA)**

**Contrast Ratios:**
- Neon Orchid on Obsidian: 4.8:1 ✓
- Ghost White on Void Gray: 12.1:1 ✓
- Electric Cyan on Obsidian: 11.3:1 ✓

**Keyboard Navigation:**
- All interactive elements: Tab-accessible
- Modals: Trap focus, Esc to close
- Terminal: Arrow keys to scroll history

**Screen Readers:**
- Live regions for terminal updates (`aria-live="polite"`)
- Agent status: `aria-label="Sentinel analyzing transaction"`
- Progress bars: Include percentage text alternatives

***

## **TECHNICAL IMPLEMENTATION NOTES**

### **Stack Recommendations**
- **Styling:** Tailwind CSS + CSS Modules for animations
- **3D Rendering:** Three.js + @react-three/fiber
- **Animations:** Framer Motion
- **WebSocket:** Socket.io-client

### **Performance Targets**
- First Contentful Paint: < 1.2s
- Time to Interactive: < 2.5s
- Lighthouse Score: 90+ (all categories)

### **Animation Libraries**
```bash
npm install framer-motion three @react-three/fiber @react-three/drei
```

***

## **DEMO FLOW (FOR VIDEO)**

**Script Timing (90 seconds):**

**0:00-0:15** — Hero Shot  
Pan across dashboard, highlight status cards pulsing

**0:15-0:30** — Input Demo  
User pastes malicious CBOR, clicks scan button (show radar animation)

**0:30-0:50** — Matrix Terminal  
Terminal slides up, agents communicate (emphasize payment flow with coin animation)

**0:50-1:10** — Danger Verdict  
Red alarm screen, shattered shield, "Transaction Blocked"

**1:10-1:30** — ThreatProof NFT  
Modal appears, 3D shield rotates, show metadata[1][2][3]

***

## **JUDGING CRITERIA ALIGNMENT**

**UI/UX Track Scorecard:**
| Criterion | Implementation | Score Target |
|-----------|----------------|--------------|
| Visual Innovation | Pink/obsidian theme, Matrix terminal, 3D NFT | 9/10 |
| User Clarity | Grandma-test simplicity, real-time feedback | 10/10 |
| Blockchain UX | Makes invisible security visible | 10/10 |
| Technical Polish | 60fps animations, accessibility compliance | 9/10 |
| Narrative Design | Security as cinematic performance | 10/10 |

**Final Notes:** This design prioritizes *feeling* over features. Users should feel like they're controlling a sophisticated defense system, even if the backend is simplified for the hackathon. The pink/obsidian/cyan palette creates premium urgency without falling into generic "hacker green" clichés.

[1](https://cardanofoundation.org/blog/layer-up-hackathon-driving-blockchain-adoption)
[2](https://dribbble.com/shots/26204909-Morpho-DeFi-Dashboard-Clean-Dark-and-Data-Rich-UI-UX)
[3](https://www.figma.com/resource-library/futuristic-fonts/)
[4](https://forum.cardano.org/t/cardano-developer-minihackathon-at-maranatha-christian-university-october-2-2024-january-17-2025/142683)
[5](https://www.emurgo.io/press-news/what-to-know-about-the-cardano-berlin-hackathon-2024/)
[6](https://www.youtube.com/watch?v=iaaGBIxnuYU)
[7](https://cardanofoundation.org/blog/cardano-summit-hackathon)
[8](https://coinlaunch.space/blog/solana-ai-hackathon-the-best-ai-agents/)
[9](https://projectcatalyst.io/funds/12/cardano-open-ecosystem/cardano-east-africa-hackathon-improving-education-through-blockchain)
[10](https://www.near.org/blog/coinbase-onchain-ai-hackathon)
[11](https://www.behance.net/gallery/176157997/UI-UX-Dashboard-Design-for-Cross-Chain-Protocol-DeFi)
[12](https://dribbble.com/search/black-and-pink-ui)
[13](https://dribbble.com/tags/obsidian)
[14](https://www.figma.com/community/file/1522238618706669989/dark-finance-crypto-dashboard-ui-design)
[15](https://octet.design/colors/user-interfaces/crypto-ui-design/)
[16](https://www.behance.net/search/projects/crypto%20app%20ui%20dark%20mode)
[17](https://www.xenonstack.com/blog/agentic-ai-data-visualisation)
[18](https://dribbble.com/search/pink-dark-mode)
[19](https://din-studio.com/best-fonts/cyberpunk-fonts/)
[20](https://clickup.com/p/ai-agents/dashboard)