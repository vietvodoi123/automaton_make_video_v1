const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");

// 👉 Lấy đối số từ dòng lệnh
const dataFile = process.argv[2] || "data.txt";
const frameDir = process.argv[3] || path.join(__dirname, "frames");

// 👉 Đường dẫn template HTML
const renderedPath = path.join(__dirname, "rendered.html");
const template = fs.readFileSync(renderedPath, "utf-8");

// 👉 Đọc dữ liệu văn bản
const segments = fs.readFileSync(dataFile, "utf-8").trim().split("\n");

// 👉 Tạo thư mục lưu frame nếu chưa có
fs.mkdirSync(frameDir, { recursive: true });

(async () => {
  // 🔧 Tối ưu khởi động Puppeteer
  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720 });

  // 🔧 Tắt animation để tăng tốc render
  await page.emulateMediaFeatures([
    { name: "prefers-reduced-motion", value: "reduce" },
  ]);

  // 👉 Tạo nội dung HTML từ template
  const html = template.replace(
    "{{LINES}}",
    segments.map((line) => `<span class="segment">${line}</span>`).join("\n")
  );

  await page.setContent(html, { waitUntil: "domcontentloaded" });
  await page.evaluate(async () => {
    await document.fonts.ready;
  });

  for (let i = 0, frameCount = 0; i < segments.length; i++) {
    const text = segments[i].trim();
    if (text === "") continue;

    // 👉 Gọi highlight và chờ kết thúc qua Promise
    await page.evaluate(async (index) => {
      if (typeof window.highlight !== "function") {
        throw new Error("❌ Hàm highlight(index) chưa được định nghĩa trong rendered.html");
      }

      await new Promise((resolve) => {
        window.__resolveCapture = resolve;
        window.highlight(index);
      });
    }, i);

    // 👉 Chụp ảnh toàn bộ khung hình 1280x720
    const framePath = path.join(
      frameDir,
      `frame${String(frameCount).padStart(4, "0")}.png`
    );

    await page.screenshot({ path: framePath });
    console.log(`✅ Đã chụp frame ${frameCount + 1}`);
    frameCount++;
  }

  await browser.close();
})();
