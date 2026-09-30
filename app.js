const R = window.RACERS || [];

let rounds = 200;
let step = 0;
let history = [];
let a = null;
let b = null;
let scores = new Map();

const $ = id => document.getElementById(id);

function reset() {
  step = 0;
  history = [];
  a = null;
  b = null;

  scores = new Map(
    R.map(x => [x.id, 1000])
  );

  $("setup").hidden = true;
  $("result").hidden = true;
  $("game").hidden = false;

  next();
}

function pick() {
  if (R.length < 2) {
    return;
  }

  const firstIndex = Math.floor(Math.random() * R.length);
  let secondIndex = Math.floor(Math.random() * R.length);

  while (secondIndex === firstIndex) {
    secondIndex = Math.floor(Math.random() * R.length);
  }

  a = R[firstIndex];
  b = R[secondIndex];
}

function next() {
  if (step >= rounds) {
    finish();
    return;
  }

  pick();
  render();
}

function render() {
  $("progress").textContent = `${step} / ${rounds}`;

  if (!a || !b) {
    return;
  }

  for (const [id, x] of [
    ["left", a],
    ["right", b]
  ]) {
    const el = $(id);

    const img = el.querySelector("img");
    const name = el.querySelector(".name");
    const meta = el.querySelector(".meta");

    img.src = x.photo;
    img.alt = x.name;

    name.textContent = x.name;

    meta.textContent =
      `${x.id}${x.grade ? "　" + x.grade : ""}`;
  }
}

function choose(winner, loser) {
  if (!winner || !loser) {
    return;
  }

  history.push([
    a,
    b,
    new Map(scores),
    step
  ]);

  const sa = scores.get(winner.id) || 1000;
  const sb = scores.get(loser.id) || 1000;

  const ea =
    1 / (1 + Math.pow(10, (sb - sa) / 400));

  const k = 24;

  scores.set(
    winner.id,
    sa + k * (1 - ea)
  );

  scores.set(
    loser.id,
    sb - k * (1 - ea)
  );

  step++;

  next();
}

function both() {
  if (!a || !b) {
    return;
  }

  history.push([
    a,
    b,
    new Map(scores),
    step
  ]);

  scores.set(
    a.id,
    (scores.get(a.id) || 1000) + 4
  );

  scores.set(
    b.id,
    (scores.get(b.id) || 1000) + 4
  );

  step++;

  next();
}

$("left").onclick = () => {
  choose(a, b);
};

$("right").onclick = () => {
  choose(b, a);
};

$("skip").onclick = () => {
  if (!a || !b) {
    return;
  }

  history.push([
    a,
    b,
    new Map(scores),
    step
  ]);

  step++;

  next();
};

$("both").onclick = both;

$("undo").onclick = () => {
  const h = history.pop();

  if (!h) {
    return;
  }

  [a, b, scores, step] = h;

  $("game").hidden = false;
  $("result").hidden = true;

  render();
};

document
  .querySelectorAll("[data-rounds]")
  .forEach(button => {
    button.onclick = () => {
      rounds = Number(button.dataset.rounds);
      reset();
    };
  });

$("again").onclick = () => {
  $("result").hidden = true;
  $("setup").hidden = false;
};

function finish() {
  $("game").hidden = true;
  $("result").hidden = false;

  const top = [...R]
    .sort(
      (x, y) =>
        (scores.get(y.id) || 0) -
        (scores.get(x.id) || 0)
    )
    .slice(0, 9);

  $("ranking").innerHTML = top
    .map((x, i) => `
      <div class="rank">
        <div class="num">${i + 1}</div>
        <img src="${x.photo}" alt="${x.name}">
        <div>
          <div class="rn">${x.name}</div>
          <div class="rm">
            ${x.id}${x.grade ? "　" + x.grade : ""}
          </div>
        </div>
      </div>
    `)
    .join("");
}

if (!R.length) {
  $("setup").innerHTML = `
    <h2>レーサーデータを読み込めませんでした</h2>
    <p class="note">
      racers.js を確認してください。
    </p>
  `;
}
