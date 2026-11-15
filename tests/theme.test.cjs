"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");
const path = require("node:path");

const source = fs.readFileSync(path.join(__dirname, "../assets/theme.js"), "utf8");

function makePage({ saved, blocked = false, hasToggle = true } = {}) {
  const attrs = new Map([["data-gc-theme", "light"]]);
  const buttonAttrs = new Map([["aria-pressed", "false"]]);
  const clicks = [];
  const writes = [];
  const label = { textContent: "Dark mode" };
  const symbol = { textContent: "☾" };
  const themeAttrs = new Map([["content", "#f6f7fb"]]);
  const root = {
    getAttribute(name) { return attrs.get(name); },
    setAttribute(name, value) { attrs.set(name, value); },
  };
  const toggle = {
    hidden: true,
    setAttribute(name, value) { buttonAttrs.set(name, value); },
    querySelector(name) {
      if (name === "[data-theme-label]") return label;
      if (name === "[data-theme-symbol]") return symbol;
      return null;
    },
    addEventListener(name, cb) {
      if (name === "click") clicks.push(cb);
    },
  };
  const document = {
    documentElement: root,
    querySelector(name) {
      if (name === "[data-theme-toggle]") return hasToggle ? toggle : null;
      if (name === 'meta[name="theme-color"]') {
        return { setAttribute(key, value) { themeAttrs.set(key, value); } };
      }
      return null;
    },
  };
  const localStorage = {
    getItem(key) {
      if (blocked) throw Error("Storage disabled");
      assert.equal(key, "goreecloud.website.appearance");
      return saved;
    },
    setItem(key, value) {
      if (blocked) throw Error("Storage disabled");
      writes.push({ key, value });
    },
  };
  vm.runInNewContext(source, { document, window: { localStorage } }, { timeout: 1200 });
  return { attrs, buttonAttrs, clicks, writes, toggle, label, symbol, themeAttrs };
}

test("fresh visitor gets light mode regardless of operating system", () => {
  const page = makePage();
  assert.equal(page.attrs.get("data-gc-theme"), "light");
  assert.equal(page.toggle.hidden, false);
  assert.equal(page.buttonAttrs.get("aria-pressed"), "false");
  assert.equal(page.buttonAttrs.get("aria-label"), "Switch to dark theme");
  assert.equal(page.label.textContent, "Dark mode");
  assert.equal(page.themeAttrs.get("content"), "#f6f7fb");
  assert.deepEqual(page.writes, []);
});

test("dark choice is explicit, keyboard-button compatible, and saved locally", () => {
  const page = makePage();
  assert.equal(page.clicks.length, 1);
  page.clicks[0]();
  assert.equal(page.attrs.get("data-gc-theme"), "dark");
  assert.equal(page.buttonAttrs.get("aria-pressed"), "true");
  assert.equal(page.buttonAttrs.get("aria-label"), "Switch to light theme");
  assert.equal(page.label.textContent, "Light mode");
  assert.equal(page.themeAttrs.get("content"), "#0d121d");
  assert.equal(page.writes[0].value, "dark");
  page.clicks[0]();
  assert.equal(page.attrs.get("data-gc-theme"), "light");
  assert.equal(page.writes[1].value, "light");
});

test("saved dark setting is respected; invalid values fall back to light", () => {
  assert.equal(makePage({ saved: "dark" }).attrs.get("data-gc-theme"), "dark");
  assert.equal(makePage({ saved: "system" }).attrs.get("data-gc-theme"), "light");
  assert.equal(makePage({ saved: "not-a-theme" }).attrs.get("data-gc-theme"), "light");
});

test("restricted storage does not break switching", () => {
  const page = makePage({ blocked: true });
  assert.equal(page.attrs.get("data-gc-theme"), "light");
  page.clicks[0]();
  assert.equal(page.attrs.get("data-gc-theme"), "dark");
});

test("404 page without appearance button can honor prior choice safely", () => {
  const page = makePage({ saved: "dark", hasToggle: false });
  assert.equal(page.attrs.get("data-gc-theme"), "dark");
  assert.equal(page.clicks.length, 0);
});

test("appearance script contains no network calls, external dependency, or telemetry", () => {
  assert.doesNotMatch(source, /\bfetch\s*\(|XMLHttpRequest|sendBeacon|document\.cookie|https?:\/\//);
});
