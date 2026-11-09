import pathlib,sys
from playwright.sync_api import sync_playwright
D=pathlib.Path(__file__).parent; out=D/"out"; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome"); pg=b.new_page(viewport={"width":2600,"height":900}); pg.goto((D/"brand.html").as_uri())
    for name,kind,W,H in [("avatar.png","avatar",800,800),("banner-bilibili.png","banner",2560,400)]:
        pg.evaluate(f"draw('{kind}',{W},{H})"); pg.locator("#s").screenshot(path=str(out/name))
    b.close()
