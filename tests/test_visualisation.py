import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "graph.html"


class StandaloneGraphPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_page_is_complete_and_offline(self):
        self.assertIn("<!doctype html>", self.html.lower())
        self.assertEqual(1, self.html.lower().count("<!doctype html>"))
        self.assertNotRegex(self.html, r"<script[^>]+src=")
        self.assertNotRegex(self.html, r"<link[^>]+href=")
        self.assertIn("D3.js v7.9.0", self.html)

    def test_embedded_graph_matches_the_neo4j_projection(self):
        match = re.search(
            r'<script id="graph-data" type="application/json">(.*?)</script>',
            self.html,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        graph = json.loads(match.group(1))
        self.assertEqual(381, len(graph["nodes"]))
        self.assertEqual(897, len(graph["links"]))
        self.assertEqual(29, len(graph["mappingExplanations"]))

        node_ids = {node["id"] for node in graph["nodes"]}
        self.assertEqual(len(graph["nodes"]), len(node_ids))
        for link in graph["links"]:
            self.assertIn(link["source"], node_ids)
            self.assertIn(link["target"], node_ids)

    def test_requested_filter_families_are_present(self):
        for filter_id in (
            "standard-categories",
            "regulation-categories",
            "governance-types",
            "data-standard-landscape",
            "data-regulation-landscape",
            "compliance-mappings",
            "ingestion-patterns",
            "ingestion-modules",
            "ingestion-components",
        ):
            self.assertIn(f'id="filter-{filter_id}"', self.html)

        self.assertNotIn('id="filter-landscape-entries"', self.html)
        self.assertIn('data-group="standardLandscapeEntry"', self.html)
        self.assertIn('data-group="regulationLandscapeEntry"', self.html)

    def test_node_and_edge_label_toggles_are_present(self):
        self.assertIn('id="toggle-node-labels"', self.html)
        self.assertIn('id="toggle-edge-labels"', self.html)
        self.assertIn('"link-label"', self.html)

    def test_edges_have_directional_arrowheads_clear_of_target_nodes(self):
        for marker_id in ("arrow-default", "arrow-compliance", "arrow-highlighted"):
            self.assertIn(f'["{marker_id}"', self.html)
            self.assertIn(f"marker-end: url(#{marker_id})", self.html)
        self.assertIn('attr("orient", "auto")', self.html)
        self.assertIn('function edgeEndpoints(item)', self.html)
        self.assertIn('const targetOffset = radii[groupFor(item.target)] + 4', self.html)

    def test_graph_can_be_frozen_and_dragged_nodes_remain_pinned(self):
        self.assertIn('id="toggle-freeze"', self.html)
        self.assertIn('aria-pressed="false"', self.html)
        self.assertIn("const pinnedPositions = new Map()", self.html)
        self.assertIn("pinnedPositions.set(item.id", self.html)
        self.assertIn("function setGraphFrozen", self.html)
        self.assertNotIn("simulation.alphaTarget(.25).restart()", self.html)
        self.assertNotIn("item.fx = null", self.html)
        self.assertNotIn("item.fy = null", self.html)

    def test_selectable_layouts_and_non_wrapping_view_controls_are_present(self):
        for layout in ("force", "hierarchy", "tree", "radial", "star"):
            self.assertRegex(
                self.html,
                rf'id="layout-{layout}"[^>]+type="radio"[^>]+name="graph-layout"[^>]+value="{layout}"',
            )
        self.assertIn("function applyStaticLayout", self.html)
        self.assertIn("function buildSpanningTree", self.html)
        self.assertIn("const layoutInputs", self.html)
        self.assertRegex(self.html, r"\.view-button\s*\{[^}]*white-space:\s*nowrap")
        self.assertIn('class="button view-button" id="reset-view"', self.html)

    def test_changing_layout_clears_manual_node_pins(self):
        self.assertIn("function changeLayout", self.html)
        self.assertRegex(
            self.html,
            r"function changeLayout\(\)\s*\{\s*pinnedPositions\.clear\(\);\s*applyFilters\(\);\s*\}",
        )
        self.assertIn('input.addEventListener("change", changeLayout)', self.html)

    def test_node_selection_highlights_its_visible_neighbourhood(self):
        self.assertIn("function highlightSelection", self.html)
        self.assertIn("dagLineageFor(selectedNodeId, links", self.html)
        self.assertIn('classed("selected"', self.html)
        self.assertIn('classed("connected"', self.html)
        self.assertIn('classed("dimmed"', self.html)
        self.assertIn('attr("aria-pressed"', self.html)
        self.assertRegex(self.html, r"\.link\.highlighted\s*\{")
        self.assertRegex(self.html, r"\.node\.selected\s+circle\s*\{")
        self.assertIn("if (selectedNodeId === item.id)", self.html)
        self.assertIn("selectedNodeId = null", self.html)

    def test_all_pipeline_types_are_selectable(self):
        for pipeline_id in (
            "batch-file-ingestion",
            "api-pull-ingestion",
            "event-driven-ingestion",
            "database-cdc-ingestion",
            "object-store-replication",
            "table-format-streaming",
        ):
            self.assertIn(f'value="pattern-type:{pipeline_id}"', self.html)

    def test_dependent_module_and_component_selectors_are_present(self):
        self.assertIn('<label for="module-select">Module</label>', self.html)
        self.assertIn('<select id="module-select">', self.html)
        self.assertIn('<option value="all">All modules</option>', self.html)
        self.assertIn('<label for="component-select">Component</label>', self.html)
        self.assertIn('<select id="component-select">', self.html)
        self.assertIn('<option value="all">All components</option>', self.html)
        self.assertIn("function populateModuleOptions", self.html)
        self.assertIn("function populateComponentOptions", self.html)
        self.assertIn("function selectionClosure", self.html)
        self.assertIn('moduleSelect.addEventListener("change"', self.html)
        self.assertIn('componentSelect.addEventListener("change"', self.html)

    def test_standard_and_regulation_category_selectors_filter_independently(self):
        self.assertIn('<label for="standard-category-select">Data standard category</label>', self.html)
        self.assertIn('<select id="standard-category-select">', self.html)
        self.assertIn('<option value="all">All data standard categories</option>', self.html)
        self.assertIn('<label for="regulation-category-select">Data regulation category</label>', self.html)
        self.assertIn('<select id="regulation-category-select">', self.html)
        self.assertIn('<option value="all">All data regulation categories</option>', self.html)
        self.assertIn("function populateCategoryOptions()", self.html)
        self.assertIn("function categorySelection()", self.html)
        self.assertIn('standardCategorySelect.addEventListener("change", applyFilters)', self.html)
        self.assertIn('regulationCategorySelect.addEventListener("change", applyFilters)', self.html)
        self.assertIn('const allowedStandardEntries = restrictLandscape(standardCategorySelect', self.html)
        self.assertIn('const allowedRegulationEntries = restrictLandscape(regulationCategorySelect', self.html)

    def test_pipeline_scope_and_accessible_alternative_are_implemented(self):
        self.assertIn("function selectionClosure", self.html)
        self.assertIn("function applyFilters", self.html)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn('id="graph-summary"', self.html)
        self.assertIn('id="reset-view"', self.html)

    def test_authoritative_sources_are_normalised_as_clickable_urls(self):
        match = re.search(
            r'<script id="graph-data" type="application/json">(.*?)</script>',
            self.html,
            flags=re.DOTALL,
        )
        graph = json.loads(match.group(1))
        mapping = next(
            node
            for node in graph["nodes"]
            if node["id"] == "component-mapping:data-contract-definition-odcs"
        )
        self.assertEqual(4, len(mapping["authoritativeSources"]))
        self.assertTrue(
            all(source.startswith("https://") for source in mapping["authoritativeSources"])
        )
        self.assertIn('class="source-link"', self.html)
        self.assertIn("Authoritative sources", self.html)

    def test_selection_details_use_a_scrollable_right_hand_panel(self):
        self.assertIn('<aside class="details"', self.html)
        self.assertRegex(
            self.html,
            r"\.layout\s*\{[^}]*grid-template-columns:\s*minmax\(260px, 320px\)\s+minmax\(0, 1fr\)\s+minmax\(260px, 340px\)",
        )
        self.assertRegex(self.html, r"\.details\s*\{[^}]*position:\s*sticky")
        self.assertRegex(self.html, r"\.details\s*\{[^}]*overflow-y:\s*auto")

    def test_component_mappings_have_display_only_rationale_and_boundaries(self):
        match = re.search(
            r'<script id="graph-data" type="application/json">(.*?)</script>',
            self.html,
            flags=re.DOTALL,
        )
        graph = json.loads(match.group(1))
        mapping_ids = {
            node["id"]
            for node in graph["nodes"]
            if "ComponentImplementationMapping" in node["labels"]
        }
        self.assertEqual(mapping_ids, set(graph["mappingExplanations"]))
        for explanation in graph["mappingExplanations"].values():
            self.assertTrue(explanation["rationale"])
            self.assertTrue(explanation["boundary"])
            self.assertTrue(explanation["sources"])
            self.assertTrue(all(source.startswith("https://") for source in explanation["sources"]))
        self.assertIn("Why this mapping?", self.html)
        self.assertIn("Boundary", self.html)
        self.assertIn("Rationale evidence", self.html)


if __name__ == "__main__":
    unittest.main()
