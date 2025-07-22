const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");
const cliProgress = require("cli-progress");

const dataFile = process.argv[2] || "data.txt";
const frameDir = process.argv[3] || path.join(__dirname, "frames");
const renderedPath = path.join(__dirname, "rendered.html");

const template = fs.readFileSync(renderedPath, "utf-8");
const segments = fs.readFileSync(dataFile, "utf-8").trim().split("\n").filter(s => s.trim() !== "");

fs.mkdirSync(frameDir, { recursive: true });

const NUM_WORKERS = 4;
const bar = new cliProgress.SingleBar({
  format: '📷 Render | {bar} | {value}/{total} | ETA: {eta_formatted}',
  barCompleteChar: '\u2588',
  barIncompleteChar: '\u2591',
  hideCursor: true
}, cliProgress.Presets.shades_classic);

let completed = 0;

async function renderWorker(workerIndex, tasks) {
  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720 });
  await page.emulateMediaFeatures([{ name: "prefers-reduced-motion", value: "reduce" }]);

  for (const { index, text } of tasks) {
    const html = template.replace(
      "{{LINES}}",
      segments.map((line, i) => {
        const cls = i === index ? "segment highlight" : "segment";
        return `<span class="${cls}">${line}</span>`;
      }).join("\n")
    );

    await page.setContent(html, { waitUntil: "domcontentloaded" });
    await page.evaluate(() => document.fonts.ready);

    await page.evaluate((index) => {
      const segments = document.querySelectorAll(".segment");
      const el = segments[index];
      if (el) {
        el.scrollIntoView({ behavior: "instant", block: "center" });
      }
    }, index);

    const framePath = path.join(frameDir, `frame${String(index).padStart(4, "0")}.png`);
    await page.screenshot({ path: framePath });

    completed++;
    bar.update(completed);
  }

  await browser.close();
}

(async () => {
  const chunked = Array.from({ length: NUM_WORKERS }, () => []);
  segments.forEach((text, i) => {
    chunked[i % NUM_WORKERS].push({ index: i, text });
  });

  bar.start(segments.length, 0);

  await Promise.all(
    chunked.map((tasks, i) => renderWorker(i + 1, tasks))
  );

  bar.stop();
  console.log("🎉 Toàn bộ frame đã render xong.");
})();
