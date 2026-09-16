/**
 * Custom Marp Engine for VS Code Preview
 *
 * Dynamically rewrites relative widget paths (e.g. `../../widgets/...`)
 * into `http://localhost:5599/widgets/...` at render time inside VS Code.
 *
 * This enables:
 * 1. Clean, canonical relative paths in Markdown source files.
 * 2. 100% native compatibility with GitHub Pages (static `dist/`).
 * 3. Working interactive widgets in VS Code side preview without iframe sandboxing errors.
 */

const { Marp } = require('@marp-team/marp-core');

function marpWidgetsPlugin(md) {
  const rewriteWidgetPaths = (html) => {
    if (!html || typeof html !== 'string') return html;
    // Matches src="../../widgets/" or src="../widgets/"
    return html.replace(
      /(src=["'])(?:\.{1,2}\/)+widgets\//g,
      '$1http://localhost:5599/widgets/'
    );
  };

  const defaultHtmlBlock = md.renderer.rules.html_block || ((tokens, idx) => tokens[idx].content);
  md.renderer.rules.html_block = (tokens, idx, options, env, self) => {
    const html = defaultHtmlBlock(tokens, idx, options, env, self);
    return rewriteWidgetPaths(html);
  };

  const defaultHtmlInline = md.renderer.rules.html_inline || ((tokens, idx) => tokens[idx].content);
  md.renderer.rules.html_inline = (tokens, idx, options, env, self) => {
    const html = defaultHtmlInline(tokens, idx, options, env, self);
    return rewriteWidgetPaths(html);
  };
}

function CustomMarpEngine(opts) {
  const marp = new Marp(opts);
  marp.use(marpWidgetsPlugin);
  return marp;
}

CustomMarpEngine.prototype = Object.create(Marp.prototype);
CustomMarpEngine.prototype.constructor = CustomMarpEngine;
CustomMarpEngine.default = CustomMarpEngine;

module.exports = CustomMarpEngine;
