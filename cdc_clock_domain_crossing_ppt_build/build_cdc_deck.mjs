import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const FINAL_PPTX = "/Users/jhpark/work/codex/CDC_기법_비교와_Reconvergence.pptx";
const PREVIEW_DIR = "/Users/jhpark/work/codex/cdc_clock_domain_crossing_ppt_build/rendered";
const LAYOUT_DIR = "/Users/jhpark/work/codex/cdc_clock_domain_crossing_ppt_build/layouts";
const W = 1280;
const H = 720;
const FONT = "Apple SD Gothic Neo";
const MONO = "Menlo";

const C = {
  canvas: "#FFFFFF",
  ink: "#111317",
  muted: "#59616C",
  panel: "#EDEDED",
  panel2: "#F6F7F8",
  rule: "#B8BCC4",
  accent: "#6DCBF4",
  blue: "#3D8DFF",
  paleBlue: "#DFF3FC",
  navy: "#14345B",
  danger: "#D63C3C",
  paleDanger: "#FDEAEA",
  green: "#187A55",
  paleGreen: "#E7F5EF",
  white: "#FFFFFF",
};

const URLS = {
  cummingsCdc: "https://www.sunburst-design.com/papers/CummingsSNUG2008Boston_CDC.pdf",
  cummingsFifo: "https://www.sunburst-design.com/papers/CummingsSNUG2002SJ_FIFO1.pdf",
  amdSingle: "https://docs.amd.com/r/2021.1-English/ug953-vivado-7series-libraries/XPM_CDC_SINGLE",
  amdArray: "https://docs.amd.com/r/en-US/pg382-xpm-cdc-generator/XPM_CDC_ARRAY_SINGLE",
  amdHandshake: "https://docs.amd.com/r/en-US/pg382-xpm-cdc-generator/XPM_CDC_HANDSHAKE",
  amdFifo: "https://docs.amd.com/r/en-US/ug1353-versal-architecture-ai-libraries/XPM_FIFO_ASYNC",
  amdRules: "https://docs.amd.com/r/en-US/ug906-vivado-design-analysis/CDC-Rules-Precedence",
  intelFifo: "https://www.intel.com/content/www/us/en/docs/programmable/683082/22-1/dual-clock-fifo-timing-constraints.html",
  intelMeta: "https://www.intel.com/content/www/us/en/docs/programmable/683068/18-1/metastability-analysis.html",
  synopsysReconvergence: "https://www.synopsys.com/content/dam/synopsys/verification/white-papers/achieving-cdc-signoff-with-hier-cdc-flow-wp.pdf",
};

async function writeBlob(path, blob) {
  await fs.writeFile(path, new Uint8Array(await blob.arrayBuffer()));
}

function rect(slide, x, y, w, h, options = {}) {
  const radius = options.radius ?? 0;
  return slide.shapes.add({
    geometry: radius ? "roundRect" : "rect",
    name: options.name,
    position: { left: x, top: y, width: w, height: h },
    fill: options.fill ?? "none",
    line: {
      style: options.lineStyle ?? "solid",
      fill: options.line ?? "none",
      width: options.lineWidth ?? (options.line && options.line !== "none" ? 1 : 0),
    },
    ...(radius ? { borderRadius: radius } : {}),
  });
}

function textBox(slide, value, x, y, w, h, size = 22, options = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    name: options.name,
    position: { left: x, top: y, width: w, height: h },
    fill: options.fill ?? "none",
    line: {
      style: "solid",
      fill: options.line ?? "none",
      width: options.line && options.line !== "none" ? (options.lineWidth ?? 1) : 0,
    },
    ...(options.radius ? { borderRadius: options.radius } : {}),
  });
  shape.text = value;
  shape.text.style = {
    fontSize: size,
    typeface: options.mono ? MONO : FONT,
    color: options.color ?? C.ink,
    bold: options.bold ?? false,
    italic: options.italic ?? false,
    alignment: options.align ?? "left",
    verticalAlignment: options.va ?? "top",
    autoFit: options.autoFit ?? "none",
  };
  return shape;
}

function rule(slide, x, y, w, color = C.rule, weight = 1) {
  return rect(slide, x, y, w, weight, { fill: color, line: "none" });
}

function vRule(slide, x, y, h, color = C.rule, weight = 1) {
  return rect(slide, x, y, weight, h, { fill: color, line: "none" });
}

function node(slide, label, x, y, w, h, options = {}) {
  const shape = rect(slide, x, y, w, h, {
    name: options.name,
    fill: options.fill ?? C.panel2,
    line: options.line ?? C.rule,
    lineWidth: options.lineWidth ?? 1.2,
    radius: options.radius ?? 8,
  });
  textBox(slide, label, x + 6, y + 8, w - 12, h - 16, options.size ?? 18, {
    bold: options.bold ?? true,
    color: options.color ?? C.ink,
    align: "center",
    va: "middle",
    mono: options.mono ?? false,
  });
  return shape;
}

function connect(slide, from, to, options = {}) {
  return slide.shapes.connect(from, to, {
    kind: options.kind ?? "straight",
    fromSide: options.fromSide ?? "right",
    toSide: options.toSide ?? "left",
    line: {
      style: options.dashed ? "dashed" : "solid",
      fill: options.color ?? C.blue,
      width: options.width ?? 2,
    },
    ...(options.noHead ? {} : { tail: { type: "triangle", width: "sm", length: "sm" } }),
    ...(options.bidirectional ? { head: { type: "triangle", width: "sm", length: "sm" } } : {}),
  });
}

function slideHeader(slide, number, title, subtitle) {
  textBox(slide, title, 52, 34, 1176, 64, 48, { bold: true, name: `slide-${number}-title` });
  if (subtitle) {
    textBox(slide, subtitle, 54, 106, 1168, 42, 22, { color: C.muted, name: `slide-${number}-subtitle` });
  }
  rule(slide, 52, 160, 1176, C.rule, 1);
}

function slideFooter(slide, number, label) {
  textBox(slide, label, 52, 668, 500, 28, 14, { bold: true, color: C.muted, va: "middle" });
  textBox(slide, String(number).padStart(2, "0"), 1160, 668, 68, 28, 14, {
    bold: true,
    color: C.muted,
    align: "right",
    va: "middle",
  });
}

function setNotes(slide, body, sources) {
  const sourceBlock = `[Sources]\n${sources.map((url) => `- ${url}`).join("\n")}`;
  slide.speakerNotes.textFrame.setText(`${body}\n\n${sourceBlock}`);
  slide.speakerNotes.setVisible(true);
}

function addBulletRows(slide, x, y, w, rows, options = {}) {
  const rowH = options.rowH ?? 48;
  rows.forEach((row, index) => {
    const rowY = y + index * rowH;
    rect(slide, x, rowY + 7, 6, 21, { fill: index === 0 ? C.blue : C.accent, line: "none" });
    textBox(slide, row, x + 17, rowY, w - 17, rowH - 3, options.size ?? 21.5, {
      color: options.color ?? C.ink,
      bold: index === 0 && (options.firstBold ?? false),
      autoFit: "shrinkText",
    });
  });
}

const deck = Presentation.create({ slideSize: { width: W, height: H } });
deck.theme.colorScheme = {
  name: "CDC Technical Grid",
  themeColors: {
    accent1: C.blue,
    accent2: C.accent,
    accent3: C.danger,
    accent4: C.green,
    accent5: C.navy,
    accent6: "#7357C7",
    bg1: C.canvas,
    bg2: C.panel2,
    tx1: C.ink,
    tx2: C.muted,
    dk1: "#000000",
    dk2: C.navy,
    lt1: C.white,
    lt2: C.panel,
    hlink: C.blue,
    folHlink: "#7357C7",
  },
};

function addSlide() {
  const slide = deck.slides.add();
  slide.background.fill = C.canvas;
  return slide;
}

// Slide 1 — three-column concept comparison, adapted from Codex Grid slide-06.
{
  const slide = addSlide();
  slideHeader(
    slide,
    1,
    "CDC는 신호의 성격과 트래픽에 맞춰 선택한다",
    "단일 상태는 2FF, 손실 없는 단건 전송은 4-phase handshake, 연속 데이터는 asynchronous FIFO가 기본 출발점이다.",
  );

  vRule(slide, 426, 188, 456, C.rule, 1);
  vRule(slide, 828, 188, 456, C.rule, 1);

  // 2FF lane.
  textBox(slide, "2FF Synchronizer", 54, 184, 350, 38, 31, { bold: true });
  textBox(slide, "1-bit level · 최소 비용", 54, 227, 350, 27, 20, { bold: true, color: C.blue });
  const ffSrc = node(slide, "SRC", 58, 277, 72, 54, { fill: C.panel2, mono: true, size: 16 });
  const ff1 = node(slide, "FF1", 151, 277, 72, 54, { fill: C.paleBlue, mono: true, color: C.navy, size: 16 });
  const ff2 = node(slide, "FF2", 244, 277, 72, 54, { fill: C.paleBlue, mono: true, color: C.navy, size: 16 });
  const ffDst = node(slide, "DST", 337, 277, 72, 54, { fill: C.panel2, mono: true, size: 16 });
  connect(slide, ffSrc, ff1);
  connect(slide, ff1, ff2);
  connect(slide, ff2, ffDst);
  textBox(slide, "metastability containment", 95, 341, 280, 24, 17, { mono: true, color: C.muted, align: "center" });
  addBulletRows(slide, 56, 382, 348, [
    "입력은 목적 클럭에 2회 이상 안정적으로 샘플되어야 한다.",
    "2개 목적지 sample stage; stage 추가 시 MTBF↑·latency↑.",
    "짧은 pulse·multi-bit bus·상관 신호 결합에는 부적합하다.",
  ], { rowH: 56, size: 21.5 });
  textBox(slide, "추천: mode/status/config 같은 저속 단일 비트", 56, 594, 348, 50, 21.5, {
    bold: true,
    color: C.navy,
    fill: C.paleBlue,
    radius: 8,
    align: "center",
    va: "middle",
  });

  // Four-phase handshake lane.
  textBox(slide, "4-phase Handshake", 452, 184, 350, 38, 31, { bold: true });
  textBox(slide, "req / ack · lossless transaction", 452, 227, 350, 27, 20, { bold: true, color: C.blue });
  const hsSrc = node(slide, "SOURCE", 468, 273, 108, 64, { fill: C.panel2, size: 17 });
  const hsDst = node(slide, "DEST", 704, 273, 108, 64, { fill: C.panel2, size: 17 });
  connect(slide, hsSrc, hsDst, { color: C.blue, width: 2.5, fromSide: "right", toSide: "left" });
  connect(slide, hsDst, hsSrc, { color: C.muted, width: 2, fromSide: "bottom", toSide: "bottom", kind: "elbow" });
  textBox(slide, "req", 594, 271, 52, 22, 17, { mono: true, bold: true, color: C.blue, align: "center" });
  textBox(slide, "ack", 594, 325, 52, 22, 17, { mono: true, bold: true, color: C.muted, align: "center" });
  textBox(slide, "req↑  →  ack↑  →  req↓  →  ack↓", 470, 348, 338, 26, 17, { mono: true, color: C.muted, align: "center" });
  addBulletRows(slide, 454, 382, 348, [
    "데이터를 hold한 채 요청하고, 목적지가 수신을 확인한다.",
    "backpressure와 lossless 전달에 유리하지만 왕복 지연이 크다.",
    "full handshake 완료 전에는 다음 전송을 시작할 수 없다.",
  ], { rowH: 56, size: 21.5 });
  textBox(slide, "추천: 드문 command/event 또는 한 건의 안정된 bus", 454, 594, 348, 50, 21.5, {
    bold: true,
    color: C.navy,
    fill: C.paleBlue,
    radius: 8,
    align: "center",
    va: "middle",
  });

  // Async FIFO lane.
  textBox(slide, "Asynchronous FIFO", 854, 184, 350, 38, 31, { bold: true });
  textBox(slide, "stream / burst · rate decoupling", 854, 227, 350, 27, 20, { bold: true, color: C.blue });
  const wr = node(slide, "WR\nCLK", 860, 273, 72, 64, { fill: C.panel2, size: 16 });
  const fifo = node(slide, "FIFO\nRAM", 984, 263, 96, 84, { fill: C.paleBlue, line: C.blue, size: 18, color: C.navy });
  const rd = node(slide, "RD\nCLK", 1132, 273, 72, 64, { fill: C.panel2, size: 16 });
  connect(slide, wr, fifo, { color: C.blue, width: 2.5 });
  connect(slide, fifo, rd, { color: C.blue, width: 2.5 });
  textBox(slide, "Gray ptr + full / empty", 900, 348, 272, 28, 16, { mono: true, color: C.muted, align: "center" });
  addBulletRows(slide, 856, 382, 348, [
    "dual-port storage가 두 클럭의 순간 속도 차이를 흡수한다.",
    "정상 구간에서는 local clock마다 1 write / 1 read가 가능하다.",
    "pointer·flag·reset·Gray skew 제약까지 함께 설계해야 한다.",
  ], { rowH: 56, size: 21.5 });
  textBox(slide, "추천: 연속·버스트 multi-word 데이터와 대역폭 분리", 856, 594, 348, 50, 21.5, {
    bold: true,
    color: C.navy,
    fill: C.paleBlue,
    radius: 8,
    align: "center",
    va: "middle",
  });

  slideFooter(slide, 1, "CDC TECHNIQUE SELECTION");
  setNotes(
    slide,
    [
      "2FF는 메타안정성이 후단으로 전파될 확률을 낮추는 구조이며, 이벤트 전달이나 bus coherency를 자동으로 보장하지 않는다.",
      "4-phase handshake의 순서는 req 상승, ack 상승, req 하강, ack 하강이다. source는 전송 중 data를 유지하고 한 번의 full handshake가 끝난 뒤 다음 transaction을 시작한다.",
      "Asynchronous FIFO는 local binary pointer와 CDC용 Gray pointer, full/empty 비교를 통해 두 clock domain의 rate를 분리한다. flag는 pointer synchronization 지연 때문에 보수적으로 반영될 수 있다.",
    ].join("\n"),
    [URLS.cummingsCdc, URLS.cummingsFifo, URLS.amdSingle, URLS.amdArray, URLS.amdHandshake, URLS.amdFifo, URLS.intelMeta],
  );
}

// Slide 2 — table-led detailed comparison, adapted from Codex Grid slide-14.
{
  const slide = addSlide();
  slideHeader(
    slide,
    2,
    "선택 기준은 데이터·손실·트래픽이다",
    "동일한 CDC 문제라도 전달 단위와 보장 수준이 다르면 최적 구조가 달라진다.",
  );

  const values = [
    ["비교 항목", "2FF Synchronizer", "4-phase Handshake", "Asynchronous FIFO"],
    ["가장 적합한 전송", "1-bit level\n(mode / status)", "단건 event 또는 안정된 bus\n(1 outstanding)", "multi-word stream / burst\n(rate decoupling)"],
    ["전달 보장", "메타안정성 확률만 저감\npulse 포착·bus 원자성은 별도", "req/ack로 수신 확인\nlossless + backpressure", "순서·버퍼링·full/empty\noverflow/underflow 방지"],
    ["지연", "2개 dst sample stage\n위상 따라 관측 cycle 가변", "forward sync + 처리 + return sync\n+ 신호 복귀: 가장 큼", "첫 word는 pointer sync + read 지연\nsteady state는 pipeline"],
    ["정상 처리율", "안정 구간마다 상태 변화\nqueue 없음", "full handshake당 1 transaction\n새 요청은 완료 후", "최대 wr_clk당 1 write\nrd_clk당 1 read"],
    ["면적 / 구현 난도", "최저: 2개 이상 FF\n+ source register 권장", "중간: 양방향 sync chain\n+ FSM/data hold", "최고: dual-port memory\n+ pointers/flags/synchronizers"],
    ["필수 검증", "ASYNC_REG·MTBF·source 등록\npulse width / 안정 시간", "data stable 동안 req active\nprotocol·reset·deadlock assertion", "Gray 1-bit transition·skew/net delay\nflag·reset·overflow assertion"],
    ["대표 실패 모드", "짧은 pulse 유실\n독립 bus sync → incoherency", "data 조기 변경·중복 요청\nreset mismatch → hang", "잘못된 full/empty·Gray skew\nreset 중 write/read → 손실"],
  ];

  const table = slide.tables.add({
    rows: values.length,
    columns: 4,
    left: 50,
    top: 181,
    width: 1180,
    height: 476,
    columnWidths: [154, 316, 350, 360],
    values,
  });

  table.borders.assign({ style: "solid", fill: C.rule, width: 1 });
  table.rows[0].height = 48;
  [58, 62, 62, 58, 58, 68, 62].forEach((height, index) => {
    table.rows[index + 1].height = height;
  });

  const allCells = table.cells.block({ row: 0, column: 0, rowCount: values.length, columnCount: 4 });
  allCells.assign({
    fill: C.white,
    textStyle: { fontSize: 21.5, typeface: FONT, color: C.ink },
    margins: { top: 5, right: 9, bottom: 5, left: 9 },
    anchor: "middle",
    horizontalOverflow: "clip",
  });

  const header = table.cells.block({ row: 0, column: 0, rowCount: 1, columnCount: 4 });
  header.assign({
    fill: C.navy,
    textStyle: { fontSize: 22, typeface: FONT, color: C.white, bold: true },
    anchor: "middle",
  });
  const rowLabels = table.cells.block({ row: 1, column: 0, rowCount: 7, columnCount: 1 });
  rowLabels.assign({
    fill: C.panel,
    textStyle: { fontSize: 21.5, typeface: FONT, color: C.ink, bold: true },
    anchor: "middle",
  });

  [2, 4, 6].forEach((row) => {
    table.cells.block({ row, column: 1, rowCount: 1, columnCount: 3 }).fill = C.panel2;
  });
  table.getCell(1, 1).fill = C.paleBlue;
  table.getCell(1, 2).fill = C.paleGreen;
  table.getCell(1, 3).fill = C.paleBlue;
  table.getCell(7, 1).fill = C.paleDanger;
  table.getCell(7, 2).fill = C.paleDanger;
  table.getCell(7, 3).fill = C.paleDanger;

  slideFooter(slide, 2, "CDC TECHNIQUE SELECTION MATRIX");
  setNotes(
    slide,
    [
      "지연 값은 두 클럭의 위상, synchronizer depth, memory read mode에 따라 달라지므로 절대 cycle 수가 아니라 구성 요소로 해석한다.",
      "2FF의 destination output은 첫 stage가 transition을 포착한 다음 stage에서 유효해진다. 추가 stage는 resolve 시간을 늘려 MTBF를 개선하지만 latency도 증가시킨다.",
      "Handshake는 정확한 전달과 backpressure를 제공하지만 full four-phase roundtrip 동안 새 transaction을 막는다. 높은 steady-state bandwidth가 필요하면 FIFO가 더 적합하다.",
      "직접 만든 asynchronous FIFO는 Gray pointer 경로에 skew와 net-delay constraint를 적용해야 한다. 단순 set_clock_groups만으로 기능 안전성이 증명되지는 않는다.",
    ].join("\n"),
    [URLS.cummingsCdc, URLS.cummingsFifo, URLS.amdSingle, URLS.amdArray, URLS.amdHandshake, URLS.amdFifo, URLS.intelFifo, URLS.intelMeta],
  );
}

// Slide 3 — reconvergence explanation, adapted from Codex Grid slide-05.
{
  const slide = addSlide();
  slideHeader(
    slide,
    3,
    "독립 2FF는 데이터 coherency를 보장하지 않는다",
    "각 경로가 메타안정성을 안전하게 가둬도, 서로 다른 cycle에 확정되면 목적지 논리는 존재하지 않았던 조합을 볼 수 있다.",
  );
  vRule(slide, 630, 188, 418, C.rule, 1);

  textBox(slide, "왜 reconvergence가 위험한가", 54, 187, 540, 36, 30, { bold: true });
  textBox(slide, "A-domain의 2-bit 상태가 01 → 10으로 바뀌는 예", 54, 229, 540, 28, 20, { color: C.muted });

  const sourceState = node(slide, "SOURCE\n01 → 10", 58, 294, 122, 86, { fill: C.panel2, size: 18, mono: true });
  const upperSync = node(slide, "bit[1]\nFF → FF", 246, 264, 144, 74, { fill: C.paleBlue, line: C.blue, size: 17, mono: true });
  const lowerSync = node(slide, "bit[0]\nFF → FF", 246, 372, 144, 74, { fill: C.paleBlue, line: C.blue, size: 17, mono: true });
  const decoder = node(slide, "DECODE\n/ FSM", 474, 318, 116, 82, { fill: C.paleDanger, line: C.danger, color: C.danger, size: 18 });
  connect(slide, sourceState, upperSync, { kind: "elbow", color: C.blue, fromSide: "right", toSide: "left" });
  connect(slide, sourceState, lowerSync, { kind: "elbow", color: C.blue, fromSide: "right", toSide: "left" });
  connect(slide, upperSync, decoder, { kind: "elbow", color: C.blue, fromSide: "right", toSide: "left" });
  connect(slide, lowerSync, decoder, { kind: "elbow", color: C.blue, fromSide: "right", toSide: "left" });
  textBox(slide, "skew", 412, 279, 60, 24, 14, { mono: true, bold: true, color: C.danger, align: "center" });

  textBox(slide, "목적지에서 관측될 수 있는 순서", 58, 478, 526, 28, 20, { bold: true });
  const stateW = 148;
  const stateX = [58, 236, 414];
  const stateLabels = [
    ["n", "01", "", C.panel2, C.ink],
    ["n + 1", "11", "illegal", C.paleDanger, C.danger],
    ["n + 2", "10", "", C.paleBlue, C.navy],
  ];
  stateLabels.forEach((item, index) => {
    rect(slide, stateX[index], 516, stateW, 74, { fill: item[3], line: index === 1 ? C.danger : C.rule, lineWidth: index === 1 ? 2 : 1, radius: 8 });
    textBox(slide, item[0], stateX[index] + 10, 524, stateW - 20, 20, 15, { mono: true, color: C.muted, align: "center" });
    textBox(slide, item[1], stateX[index] + 10, 546, stateW - 20, 25, 21, { mono: true, bold: true, color: item[4], align: "center" });
    if (item[2]) textBox(slide, item[2], stateX[index] + 10, 570, stateW - 20, 16, 13, { mono: true, bold: true, color: item[4], align: "center" });
    if (index < 2) textBox(slide, "→", stateX[index] + stateW + 7, 536, 24, 32, 24, { color: C.blue, align: "center" });
  });
  textBox(slide, "가능한 오류: 잘못된 decode, 1-cycle enable, FSM illegal transition", 58, 610, 526, 44, 21.5, {
    bold: true,
    color: C.danger,
    fill: C.paleDanger,
    radius: 8,
    align: "center",
    va: "middle",
  });

  textBox(slide, "회피 원칙", 664, 187, 540, 36, 30, { bold: true });
  const mitigations = [
    ["01", "원자성을 한 경로에 둔다", "data를 hold하고 synchronized valid/req 하나로 destination register를 load한다."],
    ["02", "encoding을 바꾼다", "counter/pointer는 Gray code로 전달하고 bit 간 skew·net delay도 제한한다."],
    ["03", "트래픽에 맞는 구조를 쓴다", "드문 단건은 handshake, 연속·버스트 데이터는 asynchronous FIFO를 사용한다."],
    ["04", "구조와 기능을 함께 검증한다", "CDC lint/report + data-stable·Gray onehot·illegal-state assertion을 결합한다."],
  ];
  mitigations.forEach((item, index) => {
    const y = 241 + index * 99;
    textBox(slide, item[0], 664, y, 48, 32, 21, { mono: true, bold: true, color: C.blue });
    textBox(slide, item[1], 724, y - 1, 480, 30, 24, { bold: true });
    textBox(slide, item[2], 724, y + 34, 480, 55, 21.5, { color: C.muted, autoFit: "shrinkText" });
    if (index < mitigations.length - 1) rule(slide, 664, y + 89, 540, C.rule, 1);
  });
  textBox(slide, "set_false_path는 coherency 증명이 아니다.", 664, 618, 540, 38, 21.5, {
    bold: true,
    color: C.navy,
    fill: C.paleBlue,
    radius: 8,
    align: "center",
    va: "middle",
  });

  slideFooter(slide, 3, "RECONVERGENCE CDC");
  setNotes(
    slide,
    [
      "Reconvergence CDC는 두 개 이상의 비동기/동기화 경로가 destination logic에서 다시 결합되는 구조다. 각 synchronizer가 개별적으로 안전해도 확정 cycle이 달라질 수 있어 correlated signal의 조합 일관성이 깨진다.",
      "대표 유형: (1) 하나의 source signal이 여러 synchronizer path로 fan-out 후 reconverge, (2) 함께 바뀌는 bus/control bits를 독립 동기화 후 decode, (3) data와 enable이 서로 다른 CDC latency를 거쳐 결합, (4) 여러 source clock의 신호가 같은 destination cone으로 fan-in.",
      "예의 01→10 전이는 실제 source에서 두 bit가 함께 바뀌어도 destination에서 01→11→10 또는 01→00→10으로 보일 수 있다. 11/00이 illegal state거나 enable decode 조건이면 spurious pulse 또는 FSM 오동작이 생긴다.",
      "완화는 synchronizer 수를 늘리는 것이 아니라 atomicity를 보존하는 protocol/encoding을 선택하는 것이다. Static CDC tool로 reconvergence/fan-out/multi-clock fan-in을 찾고, formal/SVA 및 randomized clock phase simulation으로 기능 규약을 확인한다.",
    ].join("\n"),
    [URLS.cummingsCdc, URLS.amdArray, URLS.synopsysReconvergence, URLS.amdRules, URLS.intelFifo],
  );
}

await fs.mkdir(PREVIEW_DIR, { recursive: true });
await fs.mkdir(LAYOUT_DIR, { recursive: true });
for (let index = 0; index < deck.slides.items.length; index += 1) {
  const slide = deck.slides.items[index];
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  await writeBlob(`${PREVIEW_DIR}/${stem}.png`, await deck.export({ slide, format: "png", scale: 1 }));
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(`${LAYOUT_DIR}/${stem}.layout.json`, await layout.text());
}
await writeBlob(`${PREVIEW_DIR}/montage.webp`, await deck.export({ format: "webp", montage: true, scale: 1 }));
const pptx = await PresentationFile.exportPptx(deck);
await pptx.save(FINAL_PPTX);
console.log(FINAL_PPTX);
