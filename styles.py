"""Styling constants for the digital twin Gradio app.

Palette, type, and shape are lifted directly from the portfolio's own design
system (portfolio-v2/src/index.css) so the twin reads as part of that site
rather than an embedded third-party widget: B612 / B612 Mono, near-black ink
on an off-white ground, a single amber "caution" accent, and sharp corners
instead of rounded/glass chrome.

The stylesheet below is scoped almost entirely to the elem_id/elem_classes
values set explicitly on our own gr.Blocks layout (#app-shell and its
descendants), not to Gradio's internal, version-specific DOM classes.

The one deliberate exception is the chat bubble styling under
`#chat-window .message-row ...`: Gradio's Chatbot component owns that
markup internally and doesn't expose per-bubble elem_ids, so styling the
conversation at all requires targeting the class names it renders. Those
selectors were verified directly against the installed Gradio 6.20
frontend bundle rather than guessed.
"""

INK = "oklch(21% 0.012 255)"
INK_MUTED = "oklch(43% 0.012 255)"
GROUND = "oklch(96.8% 0.003 250)"
SHEET = "oklch(99.4% 0.001 250)"
CAUTION = "oklch(72% 0.155 72)"

EXAMPLES = [
    "Tell me about your background and experience.",
    "What kinds of projects are you working on?",
    "What are your strongest technical skills?",
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=B612:ital,wght@0,400;0,700;1,400;1,700&family=B612+Mono:ital,wght@0,400;0,700;1,400&display=swap');

:root {
  --twin-ink: oklch(21% 0.012 255);
  --twin-ink-muted: oklch(43% 0.012 255);
  --twin-ink-faint: oklch(52% 0.010 255);
  --twin-rule: oklch(87% 0.005 255);
  --twin-rule-strong: oklch(21% 0.012 255);
  --twin-ground: oklch(96.8% 0.003 250);
  --twin-sheet: oklch(99.4% 0.001 250);
  --twin-caution: oklch(72% 0.155 72);
  --twin-caution-ink: oklch(38% 0.095 65);
  --twin-radius: 0.125rem;
  --twin-sans: 'B612', ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --twin-mono: 'B612 Mono', ui-monospace, 'Courier New', monospace;
}

/* ---------- Page canvas ----------
   Gradio's own root wrapper (.gradio-container) sits *above* #app-shell in
   the DOM, so painting the page background and centering the shell
   necessarily happens here rather than "inside" #app-shell. Nothing else
   about Gradio's internals is targeted by this rule. */
html, body {
  margin: 0 !important;
  background: var(--twin-ground) !important;
}
.gradio-container {
  background: var(--twin-ground) !important;
  max-width: 100% !important;
  width: 100% !important;
  padding: 0 !important;
  min-height: 100vh !important;
  font-family: var(--twin-sans) !important;
  overflow-x: hidden !important;
}
/* Gradio's own inner wrapper caps content at 1536px and adds 32px side
   padding, which stopped the shell from filling wide screens. */
.gradio-container .main {
  max-width: 100% !important;
  width: 100% !important;
  padding: 0 !important;
}
footer, .built-with, .show-api, .api-docs { display: none !important; }

/* While a response is generating, Gradio outlines each updating component
   with a 2px blue "status tracker" border. Two of them appear at different
   insets (around the chat window and around the textbox), which reads as
   misaligned boxes flashing on screen. The chat's own typing indicator
   already communicates progress, so drop this chrome. */
#app-shell [data-testid="status-tracker"] {
  border: 0 !important;
  box-shadow: none !important;
  background: transparent !important;
}

/* ---------- Force a light appearance even in dark mode ----------
   Gradio adds `.dark` to <body> from the OS/browser colour-scheme setting
   and flips its own theme variables to dark values. The Chatbot internals
   read those variables, which is what painted the conversation black and
   turned bold/heading text near-white. Rather than chase each element,
   re-point Gradio's variables at our light palette.

   Gradio declares these on `:root.dark, :root .dark` (specificity 0,2,0),
   which outranks a plain `body.dark` (0,1,1) — the `!important` flags are
   what make these overrides actually win. The dark greys are also reached
   indirectly through --neutral-*, so those are remapped too. */
body.dark {
  --background-fill-primary: var(--twin-ground) !important;
  --background-fill-secondary: var(--twin-ground) !important;
  --block-background-fill: var(--twin-sheet) !important;
  --block-border-color: var(--twin-rule) !important;
  --border-color-primary: var(--twin-rule) !important;
  --border-color-accent: var(--twin-caution) !important;
  --border-color-accent-subdued: var(--twin-caution) !important;
  --body-background-fill: var(--twin-ground) !important;
  --accordion-text-color: var(--twin-ink) !important;
  --body-text-color: var(--twin-ink) !important;
  --body-text-color-subdued: var(--twin-ink-muted) !important;
  --block-label-background-fill: var(--twin-sheet) !important;
  --block-label-text-color: var(--twin-ink) !important;
  --block-title-text-color: var(--twin-ink) !important;
  --block-info-text-color: var(--twin-ink-muted) !important;
  --link-text-color: var(--twin-caution-ink) !important;
  --input-background-fill: var(--twin-sheet) !important;
  --button-secondary-background-fill: var(--twin-sheet) !important;
  --button-secondary-text-color: var(--twin-ink) !important;
  --neutral-950: var(--twin-sheet) !important;
  --neutral-900: var(--twin-ground) !important;
  --neutral-800: var(--twin-sheet) !important;
  --neutral-700: var(--twin-rule) !important;
  --neutral-600: oklch(80% 0.005 255) !important;
  color-scheme: light;
}

/* ---------- Application shell ----------
   A flat sheet with a heavy top rule, echoing the portfolio's `.rule-head` +
   `.sheet` idiom (case-study articles open the same way) rather than a
   floating rounded card. */
#app-shell {
  box-sizing: border-box;
  max-width: none;
  width: calc(100% - 48px);
  margin: 24px auto !important;
  min-height: calc(100vh - 48px);
  border-radius: var(--twin-radius);
  border: 1px solid var(--twin-rule);
  border-top: 3px solid var(--twin-rule-strong);
  box-shadow:
    0 1px 1px color-mix(in srgb, var(--twin-ink) 4%, transparent),
    0 6px 16px -8px color-mix(in srgb, var(--twin-ink) 14%, transparent);
  background: var(--twin-sheet);
  overflow: hidden;
  display: flex !important;
  flex-direction: column !important;
  color: var(--twin-ink);
}
#app-shell * { box-sizing: border-box; min-width: 0; }

/* ---------- Topbar ---------- */
#topbar {
  flex: 0 0 auto !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 20px 32px !important;
  gap: 16px;
  border-bottom: 1px solid var(--twin-rule);
}
/* Single centred brand: a stamped square mark beside a placard-style name,
   matching the mono uppercase micro-labels used across the portfolio. */
#brand {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  width: fit-content;
  margin: 0 auto;
}
#brand-mark {
  width: 26px;
  height: 26px;
  border-radius: var(--twin-radius);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--twin-mono);
  font-weight: 700;
  font-size: 13px;
  color: var(--twin-sheet);
  background: var(--twin-ink);
}
#brand-name {
  font-family: var(--twin-mono);
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--twin-ink);
}

/* ---------- Content area (hero / prompts / chat) ---------- */
#content-area {
  flex: 1 1 auto !important;
  display: flex !important;
  flex-direction: column !important;
  min-height: 0;
  overflow: hidden;
  padding: 0 24px;
}

/* ---------- Hero ---------- */
#hero-section {
  flex: 0 0 auto !important;
  text-align: center;
  margin: clamp(24px, 6vh, 64px) auto 0;
  max-width: 640px;
}
#hero-greeting {
  margin: 0 0 48px 0;
  font-family: var(--twin-mono);
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--twin-ink-faint);
}
#hero-headline {
  margin: 0 0 30px 0;
  font-family: var(--twin-sans);
  font-size: clamp(28px, 4vw, 40px);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.2;
  color: var(--twin-ink);
}
#hero-subtext {
  margin: 0 auto;
  max-width: 500px;
  font-family: var(--twin-sans);
  font-size: 15px;
  line-height: 1.65;
  color: var(--twin-ink-muted);
}

/* ---------- Quick prompts ---------- */
/* `margin-top: auto` inside the flex column pushes the cards down so they
   sit directly above the composer instead of floating under the hero. */
#quick-prompts {
  flex: 0 0 auto !important;
  display: grid !important;
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  /* Gradio's .row sets align-items: flex-start, which stops the grid items
     from stretching — cards with fewer text lines ended up shorter. */
  align-items: stretch !important;
  gap: 16px !important;
  max-width: 920px;
  width: 100%;
  margin: auto auto 0 !important;
}
/* Gradio hides a component by adding its `hide` class (display: none).
   Our `display: grid !important` above outranked that, so the cards stayed
   on screen after the first message — re-assert the hidden state here. */
#quick-prompts.hide { display: none !important; }
.prompt-card {
  background: var(--twin-sheet) !important;
  border: 1px solid var(--twin-rule) !important;
  border-radius: var(--twin-radius) !important;
  padding: 18px 20px !important;
  min-height: 96px !important;
  height: 100% !important;
  text-align: left !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
  align-items: flex-start !important;
  gap: 10px !important;
  white-space: normal !important;
  font-family: var(--twin-sans) !important;
  font-size: 14px !important;
  font-weight: 400 !important;
  line-height: 1.5 !important;
  color: var(--twin-ink-muted) !important;
  box-shadow: none !important;
  transition: border-color 0.15s ease, transform 0.15s ease;
}
/* A stamped caution square rather than a decorative diamond — amber stays
   reserved for "actionable", the same meaning it carries site-wide. */
.prompt-card::before {
  content: '';
  display: block;
  width: 8px;
  height: 8px;
  background: var(--twin-caution);
}
.prompt-card:hover {
  border-color: var(--twin-ink) !important;
  transform: translateY(-2px);
}
.prompt-card:focus-visible {
  outline: 2px solid var(--twin-ink) !important;
  outline-offset: 2px;
}

/* ---------- Chat section ---------- */
/* The shell fills the viewport, so without a cap the conversation would
   strand against the far-left edge on wide screens. Keep it as a centred,
   readable column roughly aligned with the composer. */
#chat-section {
  flex: 1 1 auto !important;
  min-height: 0;
  width: 100%;
  max-width: 1000px;
  margin: 12px auto 0 !important;
  animation: twin-fade-in 0.2s ease;
}
#chat-window {
  height: 100% !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}
#chat-window > .label-wrap,
#chat-window > .block-label { display: none !important; }

/* Bubble styling: the one place we necessarily rely on Gradio's Chatbot
   internals (see module docstring). Scoped under #chat-window. */

/* Gradio wraps each bubble in its own `.message` element that carries a
   border, fill and 6px radius of its own — nested inside our styled
   `.message-content`, that read as a double outline around every message.
   Strip the outer layer so only our bubble is visible. */
#chat-window .message-row .message {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
}
#chat-window .message-row .message-content {
  border: 0 !important;
  box-shadow: none !important;
  border-radius: var(--twin-radius) !important;
  padding: 11px 16px !important;
  font-family: var(--twin-sans) !important;
  font-size: 14px !important;
  line-height: 1.6 !important;
}
#chat-window .message-row.user-row .message-content {
  background: var(--twin-ink) !important;
  color: var(--twin-sheet) !important;
}
#chat-window .message-row.bot-row .message-content {
  background: var(--twin-sheet) !important;
  border: 1px solid var(--twin-rule) !important;
}

/* Typing indicator. The pending assistant turn renders an empty markdown
   span; hang three animated dots off it so there's visible feedback while
   the reply is being generated (Gradio's own progress chrome is hidden
   above because it drew misaligned blue boxes). */
#chat-window .message-row.bot-row .message-content .md:empty::after {
  content: '';
  display: inline-block;
  width: 6px;
  height: 6px;
  margin: 5px 24px 5px 0;
  border-radius: 50%;
  background: var(--twin-ink-muted);
  box-shadow: 12px 0 var(--twin-ink-muted), 24px 0 var(--twin-ink-muted);
  animation: twin-typing 1.1s ease-in-out infinite;
}
@keyframes twin-typing {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

/* Gradio's theme colours headings/bold/list items explicitly, so `inherit`
   on the bubble alone isn't enough — every descendant has to be forced or
   they keep the theme's own (near-white) text colour. */
#chat-window .message-row.bot-row .message-content,
#chat-window .message-row.bot-row .message-content * {
  color: var(--twin-ink) !important;
}
#chat-window .message-row.user-row .message-content,
#chat-window .message-row.user-row .message-content * {
  color: var(--twin-sheet) !important;
}

#chat-window .message-row .message-content p { margin: 0 0 8px !important; }
#chat-window .message-row .message-content p:last-child { margin-bottom: 0 !important; }
#chat-window .message-row .message-content ul,
#chat-window .message-row .message-content ol { margin: 0 0 8px !important; }
#chat-window .message-row .message-content h1,
#chat-window .message-row .message-content h2,
#chat-window .message-row .message-content h3,
#chat-window .message-row .message-content h4 {
  font-size: 15px !important;
  font-weight: 700 !important;
  margin: 14px 0 6px !important;
}
#chat-window .message-row.bot-row .message-content a {
  color: var(--twin-caution-ink) !important;
  text-decoration: underline;
}

/* ---------- Composer ---------- */
#message-composer {
  flex: 0 0 auto !important;
  display: flex !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  gap: 10px;
  /* Matches #quick-prompts so the input lines up with the three cards. */
  max-width: 920px;
  width: calc(100% - 48px);
  margin: 20px auto 28px !important;
  padding: 6px 10px 6px 18px !important;
  background: var(--twin-sheet) !important;
  border: 1px solid var(--twin-rule) !important;
  border-radius: var(--twin-radius) !important;
  box-shadow: none !important;
  transition: border-color 0.15s ease;
}
#message-composer:focus-within {
  border-color: var(--twin-ink) !important;
}
/* Gradio wraps every component (including our plain gr.HTML icon and the
   Textbox) in a generically-themed ".block" element with its own border/
   background/padding. Scoped to the composer, strip that chrome so only
   our bar (#message-composer itself) reads as the visible container. */
#message-composer .block {
  border: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
  padding: 0 !important;
  min-width: 0 !important;
}
#message-composer > div { flex-shrink: 0; }
#message-input { flex: 1 1 auto !important; }
#message-input label { padding: 0 !important; }
#message-input textarea {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  color: var(--twin-ink) !important;
  font-family: var(--twin-sans) !important;
  font-size: 15px !important;
  padding: 10px 4px 10px 10px !important;
  min-height: 0 !important;
  resize: none !important;
}
#message-input textarea::placeholder { color: var(--twin-ink-faint) !important; }
#message-input textarea:focus { outline: none !important; box-shadow: none !important; }

/* A stamped key rather than a soft gradient pill — hovering tints it toward
   caution, the same colour the site reserves for an armed/actionable state. */
#send-button {
  flex: 0 0 40px !important;
  width: 40px !important;
  height: 40px !important;
  min-height: 0 !important;
  padding: 0 !important;
  border: 0 !important;
  border-radius: var(--twin-radius) !important;
  background: var(--twin-ink) !important;
  color: var(--twin-sheet) !important;
  font-size: 0 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: none !important;
  cursor: pointer;
  transition: background-color 0.15s ease;
}
#send-button::after {
  content: '\\2192';
  font-family: var(--twin-mono);
  font-size: 16px;
  line-height: 1;
}
#send-button:hover {
  background: color-mix(in srgb, var(--twin-ink) 85%, var(--twin-caution)) !important;
}
#send-button:focus-visible {
  outline: 2px solid var(--twin-caution) !important;
  outline-offset: 2px;
}

/* ---------- Focus states (non-color cue: visible outline everywhere) ---------- */
#app-shell button:focus-visible,
#app-shell textarea:focus-visible {
  outline: 2px solid var(--twin-ink);
  outline-offset: 2px;
}

/* ---------- Motion ---------- */
@keyframes twin-fade-in {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  #app-shell, #app-shell * { animation: none !important; transition: none !important; }
}

/* ---------- Responsive ---------- */
@media (max-width: 900px) {
  #quick-prompts { grid-template-columns: 1fr !important; }
}
@media (max-width: 640px) {
  #app-shell { width: calc(100% - 24px); margin: 12px auto !important; }
  #topbar { padding: 18px 20px !important; }
  #content-area { padding: 0 16px; }
  #hero-headline { font-size: 26px !important; }
  /* Match #content-area's 16px side padding so the composer stays flush
     with the prompt cards above it. The placeholder can't fit on one line
     at this width, so let the bar grow to two lines rather than clipping it. */
  #message-composer {
    width: calc(100% - 32px);
    padding: 8px 8px 8px 14px !important;
  }
  #message-input textarea {
    font-size: 14px !important;
    line-height: 1.4 !important;
    min-height: 42px !important;
  }
}
"""

FOCUS_JS = """
() => {
  const el = document.querySelector('#message-input textarea');
  if (el) el.focus();
}
"""
