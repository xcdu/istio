# Istio Template Recommendation Project
## Installation
First, you should clone the repo and install the dependencies.

```shell
git clone https://github/xcdu/istio.git ./istio
cd istio
pip install -r requirement.txt
```

Then you can fetch our experimental data by:

**(TBD)**

(Optional) To use scrapy-splash, you need to install and run [scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash) docker by :

```shell
docker run -p 8050:8050 scrapinghub/splash
```


## Introduction
### Architecture

The structure of the project mainly contains four stages: **crawling**, **parsing**, **preprocessing**, and **modeling**.



```mermaid
graph LR

	subgraph RawCrawling
		IstioManual --> IstioRaw
		IstioForum --> ForumRaw
	end
	
	subgraph RawParsing
		IstioRaw --> ManualRawContent
		IstioRaw --> ManualRawTemplate
		ForumRaw --> ForumRawText
		ForumRaw --> ForumRawTemplate
		ForumRaw --> ForumCategory
		ForumAnnotation
	end
	
	subgraph KnowledgeMining
		ManualRawContent -.-> ManualHyperLinkText
		ManualHyperLinkText -.-> ManualTerms
		ManualRawContent --> ManualTerms
		ManualRawContent -.-> ManualHyperLinkHierarchy
		ManualHyperLinkHierarchy -.-> ManualTermRelations
		ManualRawContent --> ManualTermRelations
		ManualTerms --> ManualKnowledgeGraph
		ManualTermRelations --> ManualKnowledgeGraph
		ManualRawContent --> Interfaces/Keys
		Interfaces/Keys
	end
	
	subgraph Preprocessing
		ManualRawContent --> ManualFormattedContent
		ForumRawText --> ForumFormattedText
		ManualRawTemplate --> ManualFormattedTemplate
		ForumRawTemplate --> ForumFormattedTemplate
	end
	
	subgraph ForumAnnotate
		ForumRaw -.-> ForumAnnotatedRaw
		ForumAnnotatedRaw -.-> ForumAnnotation
		ManualLabeling --> ForumAnnotatedRaw
	end

	subgraph Corpus
		ExternalCorpus
		ExternalCorpus -.-> WordPiecesModel
	end
	subgraph ModelInputPreparation
		ManualFormattedContent --> ManualContentModelInput
		WordPiecesModel -.-> ManualContentModelInput
		ManualFormattedTemplate --> ManualTemplateModelInput
		ForumFormattedText --> ForumTextModelInput
		WordPiecesModel -.-> ForumTextModelInput
		ForumFormattedTemplate --> ForumTemplateModelInput
		ForumCategory --> ForumCategoryModelInput
		ForumAnnotation --> ForumAnnoationModelInput
	end

	subgraph TermIdentification
		ManualContentModelInput --> TermIdentificationModel
		ManualKnowledgeGraph --> TermIdentificationModel
		TermIdentificationModel -.->|output| TermMasks
		TermMasks -.-> IdentifiedTerms
	end
	
	subgraph CategoryPrediction
	ForumTextModelInput --> CategoryPredictionModel
	ForumTemplateModelInput --> CategoryPredictionModel
	ForumCategoryModelInput --> CategoryPredictionModel
	ForumAnnoationModelInput --> CategoryPredictionModel
	CategoryPredictionModel -.->|output| PredictedCategory
	end

	subgraph TemplateGeneration
	ForumTextModelInput --> TemplateGenerationTraining
	ForumTemplateModelInput -->|loss| TemplateGenerationTraining
	PredictedCategory --> TemplateGenerationTraining
	IdentifiedTerms --> TemplateGenerationTraining
	
	TemplateGenerationTraining -->|use as| TemplateGenerationPrediction
	
	ManualContentModelInput --> TemplateGenerationPrediction
	ManualTemplateModelInput --> TemplateGenerationPrediction
	TemplateGenerationPrediction ==> FinalTemplate
	end

```
### Modules
#### Crawling

#### Parsing

#### Preprocessing

#### Modeling


