const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "麦芽";
pres.title = "评估压测系统测试文档";

// ─── Color Palette (Teal/Tech) ───
const C = {
  dark:    "1A365D",
  primary: "2B6CB0",
  accent:  "00A3C4",
  lightBg: "F7FAFC",
  white:   "FFFFFF",
  text:    "2D3748",
  muted:   "718096",
  cardBg:  "EBF8FF",
  success: "38A169",
};

// ─── Slide 1: Cover ───
let s1 = pres.addSlide();
s1.background = { color: C.dark };

// Left accent bar
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent }
});

// Tag
s1.addText("系统测试文档", {
  x: 0.7, y: 1.2, w: 5, h: 0.5,
  fontSize: 14, fontFace: "Arial", color: C.accent,
  bold: true, margin: 0
});

// Main title
s1.addText("评估压测系统\n测试文档", {
  x: 0.7, y: 1.7, w: 7, h: 1.8,
  fontSize: 40, fontFace: "Arial", color: C.white,
  bold: true, margin: 0
});

// Divider line
s1.addShape(pres.shapes.LINE, {
  x: 0.7, y: 3.6, w: 2.5, h: 0,
  line: { color: C.accent, width: 3 }
});

// Subtitle
s1.addText("涵盖模型评估与性能压测两大模块", {
  x: 0.7, y: 3.9, w: 6, h: 0.4,
  fontSize: 16, fontFace: "Arial", color: C.muted, margin: 0
});

// Bottom right deco
s1.addShape(pres.shapes.RECTANGLE, {
  x: 8.5, y: 4.5, w: 2, h: 0.06, fill: { color: C.accent, transparency: 60 }
});
s1.addShape(pres.shapes.RECTANGLE, {
  x: 9.0, y: 4.7, w: 1.5, h: 0.04, fill: { color: C.accent, transparency: 40 }
});

// ─── Slide 2: 目录 ───
let s2 = pres.addSlide();
s2.background = { color: C.white };

// Top bar
s2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.primary }
});

s2.addText("目录", {
  x: 0.6, y: 0.4, w: 5, h: 0.7,
  fontSize: 32, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

// Module cards
const modules = [
  { num: "01", title: "模型评估", desc: "评估系统地址、模型来源配置（API / 本地）、数据集来源配置", icon: "📊" },
  { num: "02", title: "性能压测", desc: "压测系统地址、模型来源配置（API / 本地）、数据集来源配置", icon: "⚡" }
];

modules.forEach((m, i) => {
  const yBase = 1.5 + i * 1.8;
  
  // Card background
  s2.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: yBase, w: 8.8, h: 1.5,
    fill: { color: C.lightBg },
    shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.08 }
  });

  // Left accent
  s2.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: yBase, w: 0.08, h: 1.5, fill: { color: C.accent }
  });

  // Number
  s2.addText(m.num, {
    x: 0.9, y: yBase + 0.15, w: 0.8, h: 1.2,
    fontSize: 36, fontFace: "Arial", color: C.accent, bold: true,
    align: "center", valign: "middle", margin: 0
  });

  // Icon
  s2.addText(m.icon, {
    x: 1.6, y: yBase + 0.25, w: 0.6, h: 1.0,
    fontSize: 28, align: "center", valign: "middle", margin: 0
  });

  // Title
  s2.addText(m.title, {
    x: 2.4, y: yBase + 0.15, w: 6.5, h: 0.5,
    fontSize: 20, fontFace: "Arial", color: C.dark, bold: true, margin: 0
  });

  // Description
  s2.addText(m.desc, {
    x: 2.4, y: yBase + 0.7, w: 6.5, h: 0.6,
    fontSize: 13, fontFace: "Arial", color: C.muted, margin: 0
  });
});

// ─── Slide 3: Module 1 - Title ───
let s3 = pres.addSlide();
s3.background = { color: C.dark };

s3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent }
});

s3.addText("模块一", {
  x: 0.7, y: 1.5, w: 4, h: 0.5,
  fontSize: 16, fontFace: "Arial", color: C.accent, bold: true, margin: 0
});

s3.addText("模型评估", {
  x: 0.7, y: 2.0, w: 7, h: 1.0,
  fontSize: 38, fontFace: "Arial", color: C.white, bold: true, margin: 0
});

s3.addShape(pres.shapes.LINE, {
  x: 0.7, y: 3.2, w: 2, h: 0,
  line: { color: C.accent, width: 2.5 }
});

s3.addText(`地址：http://10.192.161.184:5173/eval`, {
  x: 0.7, y: 3.5, w: 7, h: 0.4,
  fontSize: 14, fontFace: "Arial", color: C.muted, margin: 0
});

// ─── Slide 4: Module 1 — 模型来源（API） ───
let s4 = pres.addSlide();
s4.background = { color: C.white };

s4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.primary }
});

s4.addText("模型评估 — 模型来源", {
  x: 0.6, y: 0.3, w: 8, h: 0.7,
  fontSize: 28, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

// Section: API
s4.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.2, w: 4.2, h: 3.6,
  fill: { color: C.lightBg },
  shadow: { type: "outer", color: "000000", blur: 4, offset: 1.5, angle: 135, opacity: 0.06 }
});

s4.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.2, w: 4.2, h: 0.08, fill: { color: C.accent }
});

s4.addText("方式一：API", {
  x: 0.9, y: 1.4, w: 3.6, h: 0.5,
  fontSize: 18, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

// API details
const apiItems = [
  { label: "模型名称", value: "doubao-seed-1-6-flash-250828" },
  { label: "API Key", value: "sk-OdNlkb0nZU…" },
  { label: "Base URL", value: "https://unitoken.rodcountdi.com/v1" }
];

apiItems.forEach((item, i) => {
  const yPos = 2.1 + i * 0.85;
  s4.addText(item.label, {
    x: 0.9, y: yPos, w: 1.3, h: 0.35,
    fontSize: 11, fontFace: "Arial", color: C.muted, bold: true, margin: 0
  });
  s4.addText(item.value, {
    x: 0.9, y: yPos + 0.3, w: 3.6, h: 0.35,
    fontSize: 12, fontFace: "Arial", color: C.text, margin: 0
  });
});

// Section: Local Model
s4.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.2, w: 4.2, h: 3.6,
  fill: { color: C.lightBg },
  shadow: { type: "outer", color: "000000", blur: 4, offset: 1.5, angle: 135, opacity: 0.06 }
});

s4.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.2, w: 4.2, h: 0.08, fill: { color: C.primary }
});

s4.addText("方式二：本地模型", {
  x: 5.5, y: 1.4, w: 3.6, h: 0.5,
  fontSize: 18, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

s4.addText("路径 1", {
  x: 5.5, y: 2.1, w: 3.6, h: 0.3,
  fontSize: 11, fontFace: "Arial", color: C.accent, bold: true, margin: 0
});
s4.addText("/data/models/Qwen/Qwen2___5-0___5B-Instruct", {
  x: 5.5, y: 2.4, w: 3.6, h: 0.4,
  fontSize: 10, fontFace: "Consolas", color: C.text, margin: 0,
  valign: "top"
});

s4.addText("路径 2 (GGUF)", {
  x: 5.5, y: 3.0, w: 3.6, h: 0.3,
  fontSize: 11, fontFace: "Arial", color: C.accent, bold: true, margin: 0
});
s4.addText("/data/models/.../qwen2.5-0.5b-instruct-q4_k_m.gguf", {
  x: 5.5, y: 3.3, w: 3.6, h: 0.4,
  fontSize: 10, fontFace: "Consolas", color: C.text, margin: 0,
  valign: "top"
});

// Bottom note
s4.addText("模型：Qwen2.5-0.5B-Instruct ｜ 支持 GGUF 量化格式", {
  x: 0.6, y: 5.0, w: 8.8, h: 0.4,
  fontSize: 11, fontFace: "Arial", color: C.muted, italic: true, margin: 0
});

// ─── Slide 5: Module 1 — 数据集来源 ───
let s5 = pres.addSlide();
s5.background = { color: C.white };

s5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.primary }
});

s5.addText("模型评估 — 数据集来源", {
  x: 0.6, y: 0.3, w: 8, h: 0.7,
  fontSize: 28, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

// Left card: 官方数据集
s5.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.2, w: 4.2, h: 3.0,
  fill: { color: C.lightBg },
  shadow: { type: "outer", color: "000000", blur: 4, offset: 1.5, angle: 135, opacity: 0.06 }
});

s5.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.2, w: 4.2, h: 0.08, fill: { color: C.accent }
});

s5.addText("方式一：官方数据集", {
  x: 0.9, y: 1.45, w: 3.6, h: 0.5,
  fontSize: 17, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

s5.addText([
  { text: "ModelScope", options: { bullet: true, breakLine: true, fontSize: 14, color: C.text } },
  { text: "HuggingFace", options: { bullet: true, fontSize: 14, color: C.text } }
], {
  x: 0.9, y: 2.2, w: 3.6, h: 1.5,
  fontFace: "Arial", margin: 0, valign: "top"
});

// Right card: 本地数据集
s5.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.2, w: 4.2, h: 3.0,
  fill: { color: C.lightBg },
  shadow: { type: "outer", color: "000000", blur: 4, offset: 1.5, angle: 135, opacity: 0.06 }
});

s5.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.2, w: 4.2, h: 0.08, fill: { color: C.primary }
});

s5.addText("方式二：本地数据集", {
  x: 5.5, y: 1.45, w: 3.6, h: 0.5,
  fontSize: 17, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

const dsItems = [
  { label: "问答", path: "/data/datasets/test_qa" },
  { label: "选择题", path: "/data/datasets/test_mcq" },
  { label: "函数调用", path: "/data/datasets/test_fc" }
];

dsItems.forEach((item, i) => {
  const yPos = 2.2 + i * 0.6;
  s5.addShape(pres.shapes.RECTANGLE, {
    x: 5.5, y: yPos, w: 0.06, h: 0.45, fill: { color: C.accent }
  });
  s5.addText(item.label, {
    x: 5.8, y: yPos, w: 1, h: 0.45,
    fontSize: 12, fontFace: "Arial", color: C.dark, bold: true, margin: 0, valign: "middle"
  });
  s5.addText(item.path, {
    x: 6.8, y: yPos, w: 2.3, h: 0.45,
    fontSize: 9, fontFace: "Consolas", color: C.text, margin: 0, valign: "middle"
  });
});

// ─── Slide 6: Module 2 - Title ───
let s6 = pres.addSlide();
s6.background = { color: C.dark };

s6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent }
});

s6.addText("模块二", {
  x: 0.7, y: 1.5, w: 4, h: 0.5,
  fontSize: 16, fontFace: "Arial", color: C.accent, bold: true, margin: 0
});

s6.addText("性能压测", {
  x: 0.7, y: 2.0, w: 7, h: 1.0,
  fontSize: 38, fontFace: "Arial", color: C.white, bold: true, margin: 0
});

s6.addShape(pres.shapes.LINE, {
  x: 0.7, y: 3.2, w: 2, h: 0,
  line: { color: C.accent, width: 2.5 }
});

s6.addText(`地址：http://10.192.161.184:5173/perf`, {
  x: 0.7, y: 3.5, w: 7, h: 0.4,
  fontSize: 14, fontFace: "Arial", color: C.muted, margin: 0
});

// ─── Slide 7: Module 2 — 模型来源 ───
let s7 = pres.addSlide();
s7.background = { color: C.white };

s7.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.primary }
});

s7.addText("性能压测 — 模型来源", {
  x: 0.6, y: 0.3, w: 8, h: 0.7,
  fontSize: 28, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

// API card
s7.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.2, w: 4.2, h: 3.2,
  fill: { color: C.lightBg },
  shadow: { type: "outer", color: "000000", blur: 4, offset: 1.5, angle: 135, opacity: 0.06 }
});

s7.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.2, w: 4.2, h: 0.08, fill: { color: C.accent }
});

s7.addText("方式一：API", {
  x: 0.9, y: 1.45, w: 3.6, h: 0.5,
  fontSize: 18, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

const apiItems2 = [
  { label: "模型名称", value: "doubao-seed-1-6-flash-250828" },
  { label: "API Key", value: "sk-OdNlkb0nZU…" },
  { label: "Base URL", value: "https://unitoken.rodcountdi.com/v1" }
];

apiItems2.forEach((item, i) => {
  const yPos = 2.1 + i * 0.75;
  s7.addText(item.label, {
    x: 0.9, y: yPos, w: 1.3, h: 0.3,
    fontSize: 11, fontFace: "Arial", color: C.muted, bold: true, margin: 0
  });
  s7.addText(item.value, {
    x: 0.9, y: yPos + 0.28, w: 3.6, h: 0.3,
    fontSize: 12, fontFace: "Arial", color: C.text, margin: 0
  });
});

// Local card
s7.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.2, w: 4.2, h: 3.2,
  fill: { color: C.lightBg },
  shadow: { type: "outer", color: "000000", blur: 4, offset: 1.5, angle: 135, opacity: 0.06 }
});

s7.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.2, w: 4.2, h: 0.08, fill: { color: C.primary }
});

s7.addText("方式二：本地模型", {
  x: 5.5, y: 1.45, w: 3.6, h: 0.5,
  fontSize: 18, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

s7.addText("路径 1", {
  x: 5.5, y: 2.1, w: 3.6, h: 0.3,
  fontSize: 11, fontFace: "Arial", color: C.accent, bold: true, margin: 0
});
s7.addText("/data/models/Qwen/Qwen2___5-0___5B-Instruct", {
  x: 5.5, y: 2.4, w: 3.6, h: 0.4,
  fontSize: 10, fontFace: "Consolas", color: C.text, margin: 0, valign: "top"
});

s7.addText("路径 2 (GGUF)", {
  x: 5.5, y: 3.0, w: 3.6, h: 0.3,
  fontSize: 11, fontFace: "Arial", color: C.accent, bold: true, margin: 0
});
s7.addText("/data/models/.../qwen2.5-0.5b-instruct-q4_k_m.gguf", {
  x: 5.5, y: 3.3, w: 3.6, h: 0.4,
  fontSize: 10, fontFace: "Consolas", color: C.text, margin: 0, valign: "top"
});

// ─── Slide 8: Module 2 — 数据集来源 ───
let s8 = pres.addSlide();
s8.background = { color: C.white };

s8.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.primary }
});

s8.addText("性能压测 — 数据集来源", {
  x: 0.6, y: 0.3, w: 8, h: 0.7,
  fontSize: 28, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

// Official
s8.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.2, w: 4.2, h: 2.8,
  fill: { color: C.lightBg },
  shadow: { type: "outer", color: "000000", blur: 4, offset: 1.5, angle: 135, opacity: 0.06 }
});

s8.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.2, w: 4.2, h: 0.08, fill: { color: C.accent }
});

s8.addText("方式一：官方来源", {
  x: 0.9, y: 1.45, w: 3.6, h: 0.5,
  fontSize: 17, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

s8.addText("下拉框选择即可", {
  x: 0.9, y: 2.2, w: 3.6, h: 0.5,
  fontSize: 14, fontFace: "Arial", color: C.text, margin: 0
});

// Local
s8.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.2, w: 4.2, h: 2.8,
  fill: { color: C.lightBg },
  shadow: { type: "outer", color: "000000", blur: 4, offset: 1.5, angle: 135, opacity: 0.06 }
});

s8.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.2, w: 4.2, h: 0.08, fill: { color: C.primary }
});

s8.addText("方式二：本地数据集", {
  x: 5.5, y: 1.45, w: 3.6, h: 0.5,
  fontSize: 17, fontFace: "Arial", color: C.dark, bold: true, margin: 0
});

s8.addText("仅测试模型速度，不考虑模型效果，\n一般不用此方式", {
  x: 5.5, y: 2.2, w: 3.6, h: 1.0,
  fontSize: 12, fontFace: "Arial", color: C.muted, margin: 0
});

// ─── Slide 9: Summary ───
let s9 = pres.addSlide();
s9.background = { color: C.dark };

s9.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent }
});

s9.addText("总结", {
  x: 0.7, y: 0.5, w: 8, h: 0.7,
  fontSize: 32, fontFace: "Arial", color: C.white, bold: true, margin: 0
});

s9.addShape(pres.shapes.LINE, {
  x: 0.7, y: 1.3, w: 2, h: 0,
  line: { color: C.accent, width: 2.5 }
});

// Summary cards
const summary = [
  { label: "模型评估", items: ["API：豆包 Flash 模型", "本地：Qwen2.5-0.5B", "数据：官方 / 本地 QA/MCQ/FC"], icon: "📊" },
  { label: "性能压测", items: ["API：豆包 Flash 模型", "本地：Qwen2.5-0.5B", "数据：官方下拉选择"], icon: "⚡" }
];

summary.forEach((mod, i) => {
  const xBase = 0.7 + i * 4.6;

  s9.addShape(pres.shapes.RECTANGLE, {
    x: xBase, y: 1.7, w: 4.2, h: 3.2,
    fill: { color: C.dark, transparency: 30 },
    line: { color: C.accent, width: 1 }
  });

  s9.addText(mod.icon + "  " + mod.label, {
    x: xBase + 0.3, y: 1.9, w: 3.6, h: 0.5,
    fontSize: 18, fontFace: "Arial", color: C.accent, bold: true, margin: 0
  });

  const bulletText = mod.items.map((item, idx) => ({
    text: item,
    options: { bullet: true, breakLine: idx < mod.items.length - 1, fontSize: 13, color: C.white }
  }));

  s9.addText(bulletText, {
    x: xBase + 0.3, y: 2.5, w: 3.6, h: 2.0,
    fontFace: "Arial", margin: 0, valign: "top"
  });
});

// ─── Slide 10: Thank You ───
let s10 = pres.addSlide();
s10.background = { color: C.dark };

s10.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent }
});

s10.addText("感谢审阅", {
  x: 0.7, y: 1.8, w: 8, h: 1.2,
  fontSize: 44, fontFace: "Arial", color: C.white, bold: true, margin: 0
});

s10.addShape(pres.shapes.LINE, {
  x: 0.7, y: 3.1, w: 2.5, h: 0,
  line: { color: C.accent, width: 3 }
});

s10.addText("评估压测系统测试文档", {
  x: 0.7, y: 3.4, w: 6, h: 0.5,
  fontSize: 16, fontFace: "Arial", color: C.muted, margin: 0
});

// Save
const outputPath = "C:\\Users\\Administrator\\Desktop\\评估压测系统测试文档.pptx";
pres.writeFile({ fileName: outputPath }).then(() => {
  console.log("PPT saved to: " + outputPath);
}).catch(err => {
  console.error("Error: " + err.message);
});
