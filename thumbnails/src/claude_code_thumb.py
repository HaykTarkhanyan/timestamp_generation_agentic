"""Build the Claude Code workshop thumbnail pages (KdtXO7Pj9DI): a lyric card of Claude's
rap verse, the Claude symbol and a falling mic. Not the ML template - the user asked for
a new design (2026-10-12).

    python thumbnails/src/claude_code_thumb.py      # ~1 s, writes claude_code_{dark,light}.html

Render each page at 1280x720 with Playwright (screenshot of #t) into thumbnails/.
Fonts are the workshop's own (claude-setup/slides/fonts), embedded as base64 so each
page is standalone. The Claude symbol is Bootstrap Icons' `claude.svg` (MIT).
"""
import base64
import logging
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
Path(ROOT / "logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(),
              logging.FileHandler(ROOT / "logs" / "claude_code_thumb.log", encoding="utf-8")])
log = logging.getLogger(__name__)

FONTS = Path(r"C:\Users\hayk_\OneDrive\Desktop\misc\claude-setup\slides\fonts")
OUT = Path(__file__).resolve().parent
SPARK = ("m3.127 10.604 3.135-1.76.053-.153-.053-.085H6.11l-.525-.032-1.791-.048-1.554-.065-1.505-.08-.38-.081L0 7.832l.036-.234.32-.214.455.04 1.009.069 1.513.105 1.097.064 1.626.17h.259l.036-.105-.089-.065-.068-.064-1.566-1.062-1.695-1.121-.887-.646-.48-.327-.243-.306-.104-.67.435-.48.585.04.15.04.593.456 1.267.981 1.654 1.218.242.202.097-.068.012-.049-.109-.181-.9-1.626-.96-1.655-.428-.686-.113-.411a2 2 0 0 1-.068-.484l.496-.674L4.446 0l.662.089.279.242.411.94.666 1.48 1.033 2.014.302.597.162.553.06.17h.105v-.097l.085-1.134.157-1.392.154-1.792.052-.504.25-.605.497-.327.387.186.319.456-.045.294-.19 1.23-.37 1.93-.243 1.29h.142l.161-.16.654-.868 1.097-1.372.484-.545.565-.601.363-.287h.686l.505.751-.226.775-.707.895-.585.759-.839 1.13-.524.904.048.072.125-.012 1.897-.403 1.024-.186 1.223-.21.553.258.06.263-.218.536-1.307.323-1.533.307-2.284.54-.028.02.032.04 1.029.098.44.024h1.077l2.005.15.525.346.315.424-.053.323-.807.411-3.631-.863-.872-.218h-.12v.073l.726.71 1.331 1.202 1.667 1.55.084.383-.214.302-.226-.032-1.464-1.101-.565-.497-1.28-1.077h-.084v.113l.295.432 1.557 2.34.08.718-.112.234-.404.141-.444-.08-.911-1.28-.94-1.44-.759-1.291-.093.053-.448 4.821-.21.246-.484.186-.403-.307-.214-.496.214-.98.258-1.28.21-1.016.19-1.263.112-.42-.008-.028-.092.012-.953 1.307-1.448 1.957-1.146 1.227-.274.109-.477-.247.045-.44.266-.39 1.586-2.018.956-1.25.617-.723-.004-.105h-.036l-4.212 2.736-.75.096-.324-.302.04-.496.154-.162 1.267-.871z")

THEMES = {   # Claude's terracotta on Anthropic's near-black / ivory
    "dark": dict(bg="#141413", ink="#F0EEE6", muted="#9C9A92", bar_bg="#F0EEE6", bar_ink="#141413",
                 punch_bg="#D97757", punch_ink="#141413", glow="rgba(217,119,87,.30)"),
    "light": dict(bg="#F0EEE6", ink="#141413", muted="#6B6A64", bar_bg="#141413", bar_ink="#F0EEE6",
                  punch_bg="#D97757", punch_ink="#141413", glow="rgba(217,119,87,.22)"),
}

PAGE = """<!doctype html>
<html lang="hy"><head><meta charset="utf-8"><title>Claude Code thumbnail</title>
<style>
@font-face {{ font-family: Plex; src: url(data:font/ttf;base64,{plex}); font-weight: 600; }}
@font-face {{ font-family: PlexMono; src: url(data:font/ttf;base64,{mono}); font-weight: 500; }}
@font-face {{ font-family: NotoArm; src: url(data:font/ttf;base64,{arm}); font-weight: 600; }}
body {{ margin: 0; background: #777; }}
#t {{ width: 1280px; height: 720px; position: relative; overflow: hidden;
      background: radial-gradient(circle at 81% 28%, {glow}, transparent 42%), {bg}; }}
.tag {{ position: absolute; left: 66px; top: 44px; font: 500 24px PlexMono, monospace;
        letter-spacing: .32em; color: #D97757; }}
h1 {{ position: absolute; left: 60px; top: 70px; margin: 0; font: 600 120px/1 Plex, NotoArm, sans-serif;
      letter-spacing: -.02em; color: {ink}; }}
/* lyrics end before the logo-and-mic column at x ~1000; the script below shrinks the verse lines to fit */
.lyrics {{ position: absolute; left: 66px; top: 270px; width: 924px; font-family: Plex, NotoArm, sans-serif; }}
.lyrics p {{ margin: 0 0 16px; white-space: nowrap; }}
.lyrics span {{ font-weight: 600; padding: 2px 16px 6px; }}
.l span {{ font-size: 40px; line-height: 1.5; background: {bar_bg}; color: {bar_ink}; }}
.p span {{ font-size: 56px; line-height: 1.34; background: {punch_bg}; color: {punch_ink}; }}
.p {{ margin-top: 10px; }}
.credit {{ position: absolute; left: 68px; top: 648px; font: 500 21px PlexMono, monospace; color: {muted}; letter-spacing: .04em; }}
.spark {{ position: absolute; left: 990px; top: 36px; width: 236px; height: 236px;
          filter: drop-shadow(0 0 34px rgba(217,119,87,.55)); }}
.mic {{ position: absolute; left: 1046px; top: 424px; font: 168px/1 "Segoe UI Emoji", sans-serif;
        transform: rotate(24deg); }}
.speed {{ position: absolute; width: 9px; border-radius: 5px; background: #D97757; }}
.shadow {{ position: absolute; left: 1052px; top: 648px; width: 170px; height: 24px; border-radius: 50%;
           background: radial-gradient(ellipse, rgba(0,0,0,.40), transparent 70%); }}
</style></head><body>
<div id="t">
  <div class="tag">WORKSHOP</div>
  <h1>Claude Code</h1>
  <div class="lyrics">
    <p class="l"><span>Յո, Claude-ն եմ, անունս Շենոնից եմ ժառանգել,</span></p>
    <p class="l"><span>Դու քնած ես, ես background-ում տեստերն եմ քշում,</span></p>
    <p class="l"><span>Codex-ը դեռ մտածում ա, ես արդեն merge եմ արել,</span></p>
    <p class="p"><span>Claude Code-ն ա, ախպեր ջան։</span></p>
  </div>
  <div class="credit">Claude &middot; verse, feat. nobody</div>
  <svg class="spark" viewBox="0 0 16 16" fill="#D97757"><path d="{spark}"/></svg>
  <div class="speed" style="left:1100px; top:316px; height:70px; opacity:.85"></div>
  <div class="speed" style="left:1134px; top:302px; height:96px; opacity:.6"></div>
  <div class="speed" style="left:1168px; top:320px; height:62px; opacity:.4"></div>
  <div class="mic">&#x1F3A4;</div>
  <div class="shadow"></div>
</div>
<script>   // one font size for all verse lines: the widest one sets it
document.fonts.ready.then(() => {{
  const spans = [...document.querySelectorAll('.l span')], pad = 32;
  const max = document.querySelector('.lyrics').clientWidth;
  const widest = Math.max(...spans.map(s => s.getBoundingClientRect().width));
  if (widest > max) {{
    const size = 40 * (max - pad) / (widest - pad);
    spans.forEach(s => s.style.fontSize = size.toFixed(2) + 'px');
  }}
  document.body.dataset.fitted = '1';
}});
</script>
</body></html>
"""


def b64(name: str) -> str:
    path = FONTS / name
    if not path.is_file():
        raise FileNotFoundError(f"workshop font missing: {path}")
    return base64.b64encode(path.read_bytes()).decode("ascii")


def main() -> None:
    t0 = time.time()
    fonts = dict(plex=b64("IBMPlexSans-SemiBold.ttf"), mono=b64("IBMPlexMono-Medium.ttf"),
                 arm=b64("NotoSansArmenian-SemiBold.ttf"))
    for name, theme in THEMES.items():
        page = OUT / f"claude_code_{name}.html"
        page.write_text(PAGE.format(spark=SPARK, **fonts, **theme), encoding="utf-8")
        log.info(f"wrote {page} ({page.stat().st_size / 1024:.0f} KB)")
    log.info(f"done in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
