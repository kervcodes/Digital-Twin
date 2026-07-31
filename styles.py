"""Styling constants for the digital twin Gradio app.

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

CHARCOAL = "#2a2d3a"
CHARCOAL_MUTED = "#6b7086"
GOLD = "#ecad0a"
BLUE = "#4d8fc7"
WHITE = "#ffffff"

EXAMPLES = [
    "Tell me about your background and experience.",
    "What kinds of projects are you working on?",
    "What are your strongest technical skills?",
]

CSS = """
:root {
  --twin-charcoal: #2a2d3a;
  --twin-charcoal-muted: #6b7086;
  --twin-gold: #ecad0a;
  --twin-gold-soft: #ffcf4d;
  --twin-blue: #4d8fc7;
  --twin-page-bg: #eef0f4;
  --twin-shell-bg: #fbfaf9;
  --twin-card-bg: #ffffff;
  --twin-border: #e4e2ec;
  --twin-lavender: rgba(190, 175, 235, 0.32);
  --twin-paleblue: rgba(170, 205, 235, 0.26);
}

/* ---------- Page canvas ----------
   Gradio's own root wrapper (.gradio-container) sits *above* #app-shell in
   the DOM, so painting the muted page background and centering the shell
   necessarily happens here rather than "inside" #app-shell. Nothing else
   about Gradio's internals is targeted by this rule. */
html, body {
  margin: 0 !important;
  background: var(--twin-page-bg) !important;
}
.gradio-container {
  background: var(--twin-page-bg) !important;
  max-width: 100% !important;
  width: 100% !important;
  padding: 0 !important;
  min-height: 100vh !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
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
  --background-fill-primary: #fbfaf9 !important;
  --background-fill-secondary: #fbfaf9 !important;
  --block-background-fill: #ffffff !important;
  --block-border-color: #e4e2ec !important;
  --border-color-primary: #e4e2ec !important;
  --border-color-accent: #4d8fc7 !important;
  --border-color-accent-subdued: #4d8fc7 !important;
  --body-background-fill: #eef0f4 !important;
  --accordion-text-color: #2a2d3a !important;
  --body-text-color: #2a2d3a !important;
  --body-text-color-subdued: #6b7086 !important;
  --block-label-background-fill: #ffffff !important;
  --block-label-text-color: #2a2d3a !important;
  --block-title-text-color: #2a2d3a !important;
  --block-info-text-color: #6b7086 !important;
  --link-text-color: #4d8fc7 !important;
  --input-background-fill: #ffffff !important;
  --button-secondary-background-fill: #ffffff !important;
  --button-secondary-text-color: #2a2d3a !important;
  --neutral-950: #ffffff !important;
  --neutral-900: #fbfaf9 !important;
  --neutral-800: #ffffff !important;
  --neutral-700: #e4e2ec !important;
  --neutral-600: #c9cbd8 !important;
  color-scheme: light;
}

/* ---------- Application shell ---------- */
#app-shell {
  box-sizing: border-box;
  max-width: none;
  width: calc(100% - 48px);
  margin: 24px auto !important;
  min-height: calc(100vh - 48px);
  border-radius: 28px;
  border: 1px solid rgba(255, 255, 255, 0.7);
  box-shadow: 0 30px 80px -40px rgba(30, 20, 60, 0.22);
  background:
    radial-gradient(ellipse 720px 380px at 50% 100%, var(--twin-blue), transparent 70%),
    # radial-gradient(ellipse 520px 300px at 82% 100%, var(--twin-paleblue), transparent 65%),
    var(--twin-shell-bg);
  overflow: hidden;
  display: flex !important;
  flex-direction: column !important;
  color: var(--twin-charcoal);
}
#app-shell * { box-sizing: border-box; min-width: 0; }

/* ---------- Topbar ---------- */
#topbar {
  flex: 0 0 auto !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 24px 32px !important;
  gap: 16px;
}
/* Single centred brand: monogram stacked above the name. */
#brand {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  width: fit-content;
  margin: 0 auto;
}
#brand-mark {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  color: #ffffff;
  background: linear-gradient(135deg, var(--twin-gold), var(--twin-blue));
}
#brand-name {
  font-weight: 600;
  font-size: 15px;
  color: var(--twin-charcoal);
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
  margin: 0 0 60px 0;
  font-size: 15px;
  font-weight: 400;
  color: var(--twin-charcoal-muted);
}
#hero-headline {
  margin: 0 0 30px 0;
  font-size: clamp(28px, 4vw, 40px);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.2;
  color: var(--twin-charcoal);
}
#hero-subtext {
  margin: 0 auto;
  max-width: 500px;
  font-size: 15px;
  line-height: 1.65;
  color: var(--twin-charcoal-muted);
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
  background: rgba(255, 255, 255, 0.75) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 16px !important;
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
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 14px !important;
  font-weight: 400 !important;
  line-height: 1.5 !important;
  color: var(--twin-charcoal-muted) !important;
  box-shadow: none !important;
  transition: border-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
}
/* Decorative marker above the label, mirroring the reference layout. The
   text lives in the button label so screen readers still read it normally. */
.prompt-card::before {
  content: '\\25C6';
  font-size: 11px;
  line-height: 1;
  color: var(--twin-gold);
}
.prompt-card:hover {
  border-color: var(--twin-blue) !important;
  transform: translateY(-2px);
  box-shadow: 0 12px 28px -18px rgba(30, 20, 60, 0.35) !important;
}
.prompt-card:focus-visible {
  outline: 2px solid var(--twin-blue) !important;
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
  padding: 11px 16px !important;
  font-size: 14px !important;
  line-height: 1.6 !important;
}
#chat-window .message-row.user-row .message-content {
  background: linear-gradient(135deg, var(--twin-blue), #3f7dc0) !important;
  color: #ffffff !important;
  border-radius: 16px 16px 4px 16px !important;
}
#chat-window .message-row.bot-row .message-content {
  background: var(--twin-card-bg) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 16px 16px 16px 4px !important;
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
  background: var(--twin-charcoal-muted);
  box-shadow: 12px 0 var(--twin-charcoal-muted), 24px 0 var(--twin-charcoal-muted);
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
  color: var(--twin-charcoal) !important;
}
#chat-window .message-row.user-row .message-content,
#chat-window .message-row.user-row .message-content * {
  color: #ffffff !important;
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
  font-weight: 600 !important;
  margin: 14px 0 6px !important;
}
#chat-window .message-row.bot-row .message-content a {
  color: var(--twin-blue) !important;
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
  background: var(--twin-card-bg) !important;
  border: 1px solid #ffffff !important;
  border-radius: 999px !important;
  box-shadow: 0 10px 30px -16px rgba(30, 20, 60, 0.25);
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
#message-composer:focus-within {
  border-color: var(--twin-blue) !important;
  box-shadow: 0 0 0 3px rgba(77, 143, 199, 0.16);
}
/* Gradio wraps every component (including our plain gr.HTML icon and the
   Textbox) in a generically-themed ".block" element with its own border/
   background/padding. Scoped to the composer, strip that chrome so only
   our pill (#message-composer itself) reads as the visible container. */
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
  color: var(--twin-charcoal) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 15px !important;
  padding: 10px 4px 10px 10px !important;
  min-height: 0 !important;
  resize: none !important;
}
#message-input textarea::placeholder { color: var(--twin-charcoal-muted) !important; }
#message-input textarea:focus { outline: none !important; box-shadow: none !important; }

#send-button {
  flex: 0 0 40px !important;
  width: 40px !important;
  height: 40px !important;
  min-height: 0 !important;
  padding: 0 !important;
  border: 0 !important;
  border-radius: 50% !important;
  background: linear-gradient(135deg, var(--twin-gold), var(--twin-gold-soft)) !important;
  color: var(--twin-charcoal) !important;
  font-size: 0 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: none !important;
  cursor: pointer;
  transition: filter 0.15s ease, transform 0.15s ease;
}
#send-button::after {
  content: '\\2192';
  font-size: 16px;
  line-height: 1;
}
#send-button:hover { filter: brightness(1.06); transform: translateY(-1px); }
#send-button:focus-visible {
  outline: 2px solid var(--twin-blue) !important;
  outline-offset: 2px;
}

/* ---------- Focus states (non-color cue: visible outline everywhere) ---------- */
#app-shell button:focus-visible,
#app-shell textarea:focus-visible {
  outline: 2px solid var(--twin-blue);
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
  #app-shell { width: calc(100% - 24px); margin: 12px auto !important; border-radius: 20px; }
  #topbar { padding: 18px 20px !important; }
  #content-area { padding: 0 16px; }
  #hero-headline { font-size: 26px !important; }
  /* Match #content-area's 16px side padding so the composer stays flush
     with the prompt cards above it. The placeholder can't fit on one line
     at this width, so let the pill grow to two lines rather than clipping
     it, and soften the radius so it still reads as intentional. */
  #message-composer {
    width: calc(100% - 32px);
    padding: 8px 8px 8px 14px !important;
    border-radius: 24px !important;
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
