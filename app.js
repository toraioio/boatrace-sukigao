const R = window.RACERS || [];

const TOTAL_ROUNDS = 10;
const GROUP_SIZE = 9;

let round = 0;
let current = [];
let selected = new Set();
let counts = new Map();

const $ = id => document.getElementById(id);

function startGame() {
  round = 0;
  current = [];
  selected = new Set();

  counts = new Map(
    R.map(racer => [racer.id, 0])
  );

  $("setup").hidden = true;
  $("result").hidden = true;
  $("game").hidden = false;

  nextRound();
}

function makeGroup() {
  const shuffled = [...R];

  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }

  return shuffled.slice(0, GROUP_SIZE);
}

function nextRound() {
  if (round >= TOTAL_ROUNDS) {
    finish();
    return;
  }

  current = makeGroup();
  selected = new Set();

  round++;

  renderGroup();
}

function renderGroup() {
  $("progress").textContent =
    `${round} / ${TOTAL_ROUNDS}`;

  $("selectedCount").textContent =
    "0人選択中";

  const container = $("cards9");

  container.innerHTML = "";

  current.forEach(racer => {
    const card = document.createElement("button");

    card.className = "card9";

    card.innerHTML = `
      <img src="${racer.photo}" alt="${racer.name}">
      <div class="name">${racer.name}</div>
      <div class="meta">
        ${racer.id}${racer.grade ? "　" + racer.grade : ""}
      </div>
    `;

    card.onclick = () => {
      toggleSelection(racer, card);
    };

    container.appendChild(card);
  });

  $("next").textContent =
    round === TOTAL_ROUNDS ? "結果を見る" : "次へ";
}

function toggleSelection(racer, card) {
  if (selected.has(racer.id)) {
    selected.delete(racer.id);
    card.classList.remove("selected");
  } else {
    selected.add(racer.id);
    card.classList.add("selected");
  }

  $("selectedCount").textContent =
    `${selected.size}人選択中`;
}

function saveSelections() {
  selected.forEach(id => {
    counts.set(
      id,
      (counts.get(id) || 0) + 1
    );
  });
}

$("start").onclick = () => {
  startGame();
};

$("next").onclick = () => {
  saveSelections();
  nextRound();
};

$("again").onclick = () => {
  $("result").hidden = true;
  $("setup").hidden = false;
};

function finish() {
  $("game").hidden = true;
  $("result").hidden = false;

  const top = [...R]
    .sort((a, b) => {
      const countA = counts.get(a.id) || 0;
      const countB = counts.get(b.id) || 0;

      return countB - countA;
    })
    .slice(0, 9);

  $("ranking").innerHTML = top
    .map((racer, index) => {
      const count = counts.get(racer.id) || 0;

      return `
        <div class="rank">
          <div class="num">${index + 1}</div>

          <img
            src="${racer.photo}"
            alt="${racer.name}"
          >

          <div>
            <div class="rn">${racer.name}</div>

            <div class="rm">
              ${racer.id}${racer.grade ? "　" + racer.grade : ""}
            </div>

            <div class="rm">
              選んだ回数：${count}回
            </div>
          </div>
        </div>
      `;
    })
    .join("");
}

if (R.length < GROUP_SIZE) {
  $("setup").innerHTML = `
    <h2>レーサーデータを読み込めませんでした</h2>
    <p class="note">
      racers.js を確認してください。
    </p>
  `;
}
