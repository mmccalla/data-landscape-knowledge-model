// Derived from the MIT-licensed Data Landscape sources; see ATTRIBUTION.md and LICENSE.
// Neo4j 5.x/current Cypher. Source identifiers are unique within each landscape, not across both landscapes.
CREATE CONSTRAINT standard_entry_id_unique IF NOT EXISTS FOR (n:DataStandardLandscapeEntry) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT regulation_entry_id_unique IF NOT EXISTS FOR (n:DataRegulationLandscapeEntry) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT assessment_id_unique IF NOT EXISTS FOR (n:LandscapeAssessment) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT mapping_id_unique IF NOT EXISTS FOR (n:ComplianceMapping) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (n:Concept) REQUIRE n.id IS UNIQUE;
CREATE INDEX landscape_entry_name IF NOT EXISTS FOR (n:LandscapeEntry) ON (n.name);
CREATE INDEX landscape_entry_release_year IF NOT EXISTS FOR (n:LandscapeEntry) ON (n.firstReleaseYear);
CREATE INDEX standard_entry_name IF NOT EXISTS FOR (n:DataStandardLandscapeEntry) ON (n.name);
CREATE INDEX regulation_entry_name IF NOT EXISTS FOR (n:DataRegulationLandscapeEntry) ON (n.name);
CREATE INDEX concept_name IF NOT EXISTS FOR (n:Concept) ON (n.name);
CREATE FULLTEXT INDEX landscape_entry_search IF NOT EXISTS FOR (n:LandscapeEntry) ON EACH [n.name, n.fullName, n.description, n.governanceStatement, n.statusStatement, n.whyAStandard];
CREATE FULLTEXT INDEX assessment_search IF NOT EXISTS FOR (n:LandscapeAssessment) ON EACH [n.judgementReason];
