// Derived from the MIT-licensed Data Landscape sources; see ATTRIBUTION.md and LICENSE.
// Neo4j 5.x/current Cypher. Source identifiers are unique within each landscape, not across both landscapes.
CREATE CONSTRAINT standard_entry_id_unique IF NOT EXISTS FOR (n:DataStandardLandscapeEntry) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT regulation_entry_id_unique IF NOT EXISTS FOR (n:DataRegulationLandscapeEntry) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT assessment_id_unique IF NOT EXISTS FOR (n:LandscapeAssessment) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT mapping_id_unique IF NOT EXISTS FOR (n:ComplianceMapping) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT component_mapping_id_unique IF NOT EXISTS FOR (n:ComponentImplementationMapping) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT pattern_type_id_unique IF NOT EXISTS FOR (n:DataIngestionPatternType) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT module_type_id_unique IF NOT EXISTS FOR (n:DataPipelineModuleType) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT component_type_id_unique IF NOT EXISTS FOR (n:DataPipelineComponentType) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT attestation_id_unique IF NOT EXISTS FOR (n:Attestation) REQUIRE n.attestationId IS UNIQUE;
CREATE CONSTRAINT actor_id_unique IF NOT EXISTS FOR (n:Actor) REQUIRE n.actorId IS UNIQUE;
CREATE CONSTRAINT action_id_unique IF NOT EXISTS FOR (n:Action) REQUIRE n.actionId IS UNIQUE;
CREATE CONSTRAINT risk_id_unique IF NOT EXISTS FOR (n:Risk) REQUIRE n.riskId IS UNIQUE;
CREATE CONSTRAINT control_id_unique IF NOT EXISTS FOR (n:Control) REQUIRE n.controlId IS UNIQUE;
CREATE CONSTRAINT evidence_id_unique IF NOT EXISTS FOR (n:ControlEvidence) REQUIRE n.evidenceId IS UNIQUE;
CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (n:Concept) REQUIRE n.id IS UNIQUE;
CREATE INDEX landscape_entry_name IF NOT EXISTS FOR (n:LandscapeEntry) ON (n.name);
CREATE INDEX landscape_entry_release_year IF NOT EXISTS FOR (n:LandscapeEntry) ON (n.firstReleaseYear);
CREATE INDEX standard_entry_name IF NOT EXISTS FOR (n:DataStandardLandscapeEntry) ON (n.name);
CREATE INDEX regulation_entry_name IF NOT EXISTS FOR (n:DataRegulationLandscapeEntry) ON (n.name);
CREATE INDEX attestation_pipeline_id IF NOT EXISTS FOR (n:Attestation) ON (n.pipelineId);
CREATE INDEX attestation_module_id IF NOT EXISTS FOR (n:Attestation) ON (n.moduleId);
CREATE INDEX attestation_component_id IF NOT EXISTS FOR (n:Attestation) ON (n.componentId);
CREATE INDEX concept_name IF NOT EXISTS FOR (n:Concept) ON (n.name);
CREATE FULLTEXT INDEX landscape_entry_search IF NOT EXISTS FOR (n:LandscapeEntry) ON EACH [n.name, n.fullName, n.description, n.governanceStatement, n.statusStatement, n.whyAStandard];
CREATE FULLTEXT INDEX assessment_search IF NOT EXISTS FOR (n:LandscapeAssessment) ON EACH [n.judgementReason];
