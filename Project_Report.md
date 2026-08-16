# BLOCKCHAIN-ENABLED TRANSPARENT AND TAMPER-PROOF CARBON CREDIT TRADING PLATFORM USING SMART CONTRACT AUTOMATION AND AI-BASED EMISSION PREDICTION

---

### A Project Report

Submitted in partial fulfillment of the requirements for the award of the degree of

**Bachelor of Engineering / Bachelor of Technology**

in

**Computer Science and Engineering**

---

## CERTIFICATE

This is to certify that the project report entitled **"Blockchain-Enabled Transparent and Tamper-Proof Carbon Credit Trading Platform using Smart Contract Automation and AI-Based Emission Prediction"** is a bonafide record of the work carried out by the undersigned candidates under the guidance of the faculty advisor during the academic year 2025–2026.

---

## ACKNOWLEDGEMENT

We would like to express our sincere gratitude to our project guide for providing guidance, support, and encouragement throughout the development of this project. We also thank the Head of Department and all faculty members of the Department of Computer Science and Engineering for their continuous support. We extend our appreciation to all those who have directly or indirectly contributed to the successful completion of this project.

---

## ABSTRACT

Climate change remains one of the most pressing global challenges, with industrial greenhouse gas emissions—including Carbon Dioxide (CO₂), Methane (CH₄), and Nitrous Oxide (N₂O)—being a major contributor. To combat this, governments worldwide have introduced carbon credit systems based on the Cap-and-Trade mechanism, where industries that emit below a permitted baseline earn tradable credits, while those exceeding the limit must purchase credits to achieve compliance.

However, traditional carbon credit markets are plagued by data manipulation, fake reporting, lack of transparency, delayed verification, and trust deficits between participating entities. This project addresses these challenges by leveraging Blockchain Technology and Smart Contract Automation to build a decentralized, transparent, and tamper-proof carbon credit trading ecosystem.

The proposed platform integrates three core technological pillars: (i) an Ethereum-based blockchain layer for immutable transaction recording and token-based credit management, (ii) Solidity smart contracts for automated credit allocation, penalty assessment, and peer-to-peer trading, and (iii) an AI-powered emission prediction engine that uses historical data analytics and compound growth modeling to forecast future industrial emissions. Each carbon credit is tokenized as a digital asset on the Ethereum blockchain, where 1 token equals 1 ton of CO₂ equivalent reduction, and every transaction is permanently recorded on an immutable public ledger, eliminating the possibility of fraud or double-spending.

The platform is built using Flask (Python) for the web application layer, SQLite with SQLAlchemy ORM for relational data storage, Solidity for smart contract development, Web3.py for blockchain interaction, and Scikit-learn/NumPy for AI-powered emission prediction analytics. The system supports industry registration with admin approval, emission reporting with document verification, automated credit minting via smart contracts, a dynamic marketplace for carbon credit trading, penalty offset through token burning, credit retirement with certificate generation, and comprehensive dashboards for both industries and administrators.

**Keywords:** Blockchain, Carbon Credits, Smart Contracts, Ethereum, AI Prediction, Cap-and-Trade, Emission Monitoring, Solidity, Flask, Web3.py

---

## TABLE OF CONTENTS

1. [Introduction](#chapter-1-introduction)
2. [Literature Survey](#chapter-2-literature-survey)
3. [System Analysis](#chapter-3-system-analysis)
4. [Project Architecture](#chapter-4-project-architecture)
5. [Methodology](#chapter-5-methodology)
6. [Model](#chapter-6-model)
7. [Software Description](#chapter-7-software-description)
8. [System Testing](#chapter-8-system-testing)
9. [Results](#chapter-9-results)
10. [Reference and Bibliography](#chapter-10-reference-and-bibliography)

---

## LIST OF FIGURES

| Figure No. | Title |
|------------|-------|
| 4.1 | Overall System Architecture |
| 4.2 | Three-Tier Architecture Diagram |
| 4.3 | Smart Contract Interaction Flow |
| 4.4 | AI-Blockchain-Web Integration Diagram |
| 5.1 | System Workflow Flowchart |
| 5.2 | Emission Reporting Process Flow |
| 5.3 | Carbon Credit Trading Sequence |
| 6.1 | AI Prediction Model Pipeline |
| 6.2 | Compound Growth Projection Curve |

---

## LIST OF TABLES

| Table No. | Title |
|-----------|-------|
| 3.1 | Comparison of Existing and Proposed Systems |
| 3.2 | Feasibility Study Summary |
| 7.1 | Technology Stack Overview |
| 7.2 | Software Requirements |
| 7.3 | Hardware Requirements |
| 8.1 | Unit Test Cases |
| 8.2 | Integration Test Cases |
| 8.3 | Functional Test Cases |
| 8.4 | Blockchain Transaction Test Cases |

---

## LIST OF ABBREVIATIONS

| Abbreviation | Full Form |
|-------------|-----------|
| AI | Artificial Intelligence |
| ABI | Application Binary Interface |
| API | Application Programming Interface |
| CCT | CarbonCredit Token |
| CO₂ | Carbon Dioxide |
| CH₄ | Methane |
| CSS | Cascading Style Sheets |
| dApp | Decentralized Application |
| ERC-20 | Ethereum Request for Comments 20 |
| ETH | Ether (Ethereum cryptocurrency) |
| GHG | Greenhouse Gas |
| HTML | HyperText Markup Language |
| HTTP | HyperText Transfer Protocol |
| JSON | JavaScript Object Notation |
| ML | Machine Learning |
| N₂O | Nitrous Oxide |
| ORM | Object-Relational Mapping |
| RPC | Remote Procedure Call |
| SQL | Structured Query Language |
| UI | User Interface |

---

# CHAPTER 1: INTRODUCTION

## 1.1 Background of Carbon Credits

Climate change has emerged as one of the most significant existential threats facing humanity in the twenty-first century. The Intergovernmental Panel on Climate Change (IPCC) has consistently warned that unchecked greenhouse gas (GHG) emissions—primarily Carbon Dioxide (CO₂), Methane (CH₄), and Nitrous Oxide (N₂O)—are driving unprecedented global warming, leading to rising sea levels, extreme weather events, biodiversity loss, and socio-economic disruptions. In response to these alarming trends, international agreements such as the Kyoto Protocol (1997) and the Paris Agreement (2015) have established frameworks for nations to collectively reduce their carbon footprints.

Central to these frameworks is the concept of **carbon credits**, a market-based mechanism designed to incentivize emission reductions. Under the Cap-and-Trade model, a regulatory authority sets a cap—an upper limit—on the total amount of greenhouse gases that can be emitted by participating industries within a jurisdiction. Each industry is allocated or required to hold emission permits (credits) corresponding to their allowed emissions. Industries that reduce their emissions below the capped level earn surplus credits, which they can sell on the carbon market. Conversely, industries that exceed their permitted emissions must purchase additional credits from those with surpluses, effectively paying for the right to pollute.

One carbon credit typically represents the right to emit one metric ton of carbon dioxide equivalent (tCO₂e). This system creates a financial incentive for industries to invest in cleaner technologies, improve energy efficiency, and adopt sustainable practices. The global carbon market has experienced significant growth, with the World Bank reporting that carbon pricing initiatives now cover approximately 23% of global GHG emissions across 46 national and 36 sub-national jurisdictions.

## 1.2 Need for Transparent Carbon Credit Systems

Despite the theoretical elegance of carbon credit systems, their practical implementation has been fraught with challenges that undermine their effectiveness and credibility:

**Data Manipulation and Fraud:** Industries may underreport their actual emissions or fabricate reduction claims to earn undeserved credits. The lack of robust verification mechanisms in traditional systems makes it difficult to detect such fraudulent activities. Several high-profile cases of emission data manipulation have eroded public trust in carbon markets.

**Double Counting and Double Spending:** In the absence of a unified, immutable ledger, the same emission reduction may be claimed by multiple parties, or the same carbon credit may be sold to more than one buyer. This double-counting problem inflates the apparent environmental benefits while providing no real emission reductions.

**Lack of Transparency:** Traditional carbon credit systems often operate through centralized intermediaries—registries, brokers, and verification bodies—that maintain proprietary databases. This opacity makes it challenging for stakeholders to independently verify the authenticity, provenance, and retirement status of carbon credits.

**High Transaction Costs:** The involvement of multiple intermediaries in the verification, certification, and trading of carbon credits introduces significant transaction costs, which disproportionately burden smaller industries and developing nations.

**Delayed Verification:** Manual verification processes for emission reports are time-consuming, often taking weeks or months. This delay reduces the responsiveness of the system and creates opportunities for gaming.

**Trust Deficit:** The centralized nature of existing systems means that all participants must trust the central authority to manage the system fairly and accurately. Any compromise of this central authority—through corruption, incompetence, or cyberattack—can undermine the entire system.

These systemic weaknesses underscore the urgent need for a technological solution that can provide tamper-proof data integrity, real-time verification, transparent transactions, and automated compliance enforcement.

## 1.3 Role of Blockchain and AI

### 1.3.1 Blockchain Technology

Blockchain technology offers a transformative solution to the trust and transparency challenges plaguing carbon credit systems. A blockchain is a distributed, immutable ledger that records transactions across a network of computers in a way that makes retroactive alteration practically impossible. Key properties of blockchain that make it suitable for carbon credit management include:

- **Immutability:** Once a transaction is recorded on the blockchain, it cannot be altered or deleted, ensuring the integrity of emission records and credit transactions.
- **Transparency:** All participants can view the complete transaction history, enabling independent verification and public auditability.
- **Decentralization:** The absence of a single point of control eliminates the risk of central authority compromise and reduces dependency on intermediaries.
- **Smart Contracts:** Self-executing contracts with the terms of the agreement directly written in code enable automated enforcement of business rules, such as credit allocation, penalty assessment, and trade settlement.
- **Tokenization:** Carbon credits can be represented as digital tokens on the blockchain, enabling efficient, secure, and traceable peer-to-peer trading.

### 1.3.2 Artificial Intelligence

Artificial Intelligence (AI) complements blockchain technology by providing intelligent data analysis and predictive capabilities:

- **Emission Prediction:** AI models can analyze historical emission data to forecast future emissions, enabling industries to proactively plan their compliance strategies.
- **Data Validation:** AI algorithms can detect anomalies and inconsistencies in reported emission data, flagging potentially fraudulent submissions for further investigation.
- **Decision Support:** Predictive analytics help regulatory authorities make informed decisions about baseline adjustments, market interventions, and policy formulation.

The synergistic combination of blockchain and AI creates a robust ecosystem where AI provides intelligent data processing and prediction, while blockchain ensures the integrity and transparency of all transactions and records.

## 1.4 Objectives of the Project

The primary objectives of this project are as follows:

1. **To develop a decentralized carbon credit trading platform** that leverages Ethereum blockchain technology for tamper-proof transaction recording and credit management.

2. **To implement smart contracts** for automated carbon credit allocation, penalty assessment, and peer-to-peer trading, eliminating the need for intermediaries.

3. **To integrate AI-based emission prediction** capabilities that analyze historical data and forecast future industrial emissions using compound growth modeling.

4. **To create a transparent marketplace** where industries can securely trade carbon credits with real-time dynamic pricing based on supply and demand.

5. **To implement an automated incentive and penalty system** that rewards industries for emission reductions below baseline (by minting credit tokens) and penalizes those exceeding limits.

6. **To provide comprehensive dashboards and analytics** for both industries and administrators, enabling data-driven decision making.

7. **To ensure data integrity through document verification** workflows where admin authorities validate industry-submitted emission documents before processing.

8. **To demonstrate the practical viability** of combining blockchain, smart contracts, and AI in addressing real-world environmental governance challenges.

---

# CHAPTER 2: LITERATURE SURVEY

## 2.1 Existing Carbon Credit Trading Systems

Carbon credit trading has evolved significantly since the establishment of the Kyoto Protocol in 1997. Several systems and platforms have been developed to facilitate the trading of carbon credits at national and international levels.

**The European Union Emission Trading System (EU ETS)** is the world's first and largest carbon market, established in 2005. Operating on a Cap-and-Trade principle, the EU ETS covers approximately 40% of the EU's greenhouse gas emissions from more than 11,000 heavy energy-using installations and airlines. Despite its scale, the EU ETS has faced challenges including price volatility, over-allocation of allowances in its early phases, and vulnerability to fraud through VAT carousel schemes and the theft of carbon allowances from national registries [1].

**The Clean Development Mechanism (CDM)**, established under Article 12 of the Kyoto Protocol, allows emission-reduction projects in developing countries to earn Certified Emission Reduction (CER) credits, which can be traded and used by industrialized countries to meet their emission targets. However, the CDM has been criticized for its complex and costly project approval process, concerns about the "additionality" of emission reductions, and instances of fraudulent project claims [2].

**Voluntary carbon markets** such as the Verified Carbon Standard (VCS) and Gold Standard operate alongside compliance markets, allowing organizations to voluntarily offset their carbon footprint. These markets face challenges related to inconsistent standards, verification difficulties, and concerns about the permanence of offset projects [3].

**The Regional Greenhouse Gas Initiative (RGGI)** in the United States represents a cooperative effort among northeastern and mid-Atlantic states to cap and reduce CO₂ emissions from the power sector. While RGGI has demonstrated measurable emission reductions, its limited geographic scope and sector coverage restrict its overall impact [4].

## 2.2 Blockchain Applications in Environmental Monitoring

The application of blockchain technology to environmental monitoring and carbon credit management has garnered significant research attention in recent years.

Khaqqi et al. (2018) proposed a blockchain-based emissions trading system that uses a reputation-based approach to ensure participants' compliance with emission reduction targets. Their system addresses the challenge of fraudulent reporting by linking participants' trading privileges to their compliance records, which are stored on an immutable blockchain ledger [5].

Pan et al. (2019) developed a carbon trading model based on blockchain technology, demonstrating how smart contracts can automate the allocation, transfer, and retirement of carbon credits. Their work highlights the potential of blockchain to reduce transaction costs by 30–50% compared to traditional intermediary-based systems [6].

Hartmann and Thomas (2020) explored the use of blockchain for environmental sustainability, focusing on supply chain transparency and carbon footprint tracking. Their research demonstrated that blockchain-based systems could significantly improve the traceability and verification of environmental claims [7].

Al Sadawi et al. (2021) presented a comprehensive framework for a blockchain-based carbon emission trading platform that integrates Internet of Things (IoT) sensors for real-time emission monitoring with blockchain-based recording. Their system eliminates manual emission reporting, reducing the potential for data manipulation [8].

Richardson and Xu (2020) analyzed the energy consumption implications of blockchain-based carbon trading systems, proposing energy-efficient consensus mechanisms that make blockchain deployment more environmentally sustainable [9].

## 2.3 AI in Emission Prediction

Artificial Intelligence and Machine Learning techniques have been extensively applied to environmental data analysis and emission prediction.

Li et al. (2019) applied Long Short-Term Memory (LSTM) neural networks to predict CO₂ emissions from industrial processes, achieving prediction accuracies exceeding 95%. Their model incorporated multiple input parameters including production volume, energy consumption, and meteorological data to generate multi-step emission forecasts [10].

Wen and Yuan (2020) compared various machine learning algorithms—including Linear Regression, Support Vector Regression, Random Forest, and Gradient Boosting—for predicting carbon emissions at the city level. Their findings indicated that ensemble methods outperformed individual models, with Random Forest achieving the lowest mean absolute error [11].

Huang et al. (2021) developed a hybrid AI model combining deep learning with time-series analysis for predicting industrial greenhouse gas emissions. Their approach integrated economic indicators, energy consumption data, and historical emission records to produce accurate multi-year forecasts [12].

Sun et al. (2022) explored the integration of AI prediction models with blockchain systems for carbon credit management, demonstrating how AI-generated forecasts stored on blockchain can serve as trusted reference points for emission baseline adjustments and policy planning [13].

## 2.4 Limitations of Existing Systems

Based on the literature review, the following limitations of existing carbon credit systems have been identified:

1. **Centralization Risks:** Most existing systems rely on centralized registries and verification bodies, creating single points of failure and trust dependencies.

2. **Manual Verification Delays:** Traditional emission verification processes are labor-intensive and slow, creating a lag between emission reporting and credit allocation.

3. **Lack of Automation:** Credit allocation, penalty assessment, and trading in existing systems typically require manual intervention, increasing costs and processing time.

4. **Limited Predictive Capabilities:** Existing platforms generally lack integrated AI-based tools to help industries forecast their future emissions and plan compliance strategies proactively.

5. **Opacity in Pricing:** Market pricing mechanisms in existing systems are often opaque, with limited visibility into the factors driving price changes.

6. **Fragmentation:** The existence of multiple, incompatible carbon credit registries creates challenges for cross-border trading and increases the risk of double counting.

7. **High Entry Barriers:** Complex registration, verification, and trading processes discourage participation by small and medium enterprises.

8. **Insufficient Fraud Prevention:** Despite regulatory oversight, existing systems remain vulnerable to various forms of fraud, including emission data manipulation and credit laundering.

The proposed system addresses these limitations by combining blockchain immutability, smart contract automation, and AI-based prediction in a unified, transparent platform.

---

# CHAPTER 3: SYSTEM ANALYSIS

## 3.1 Existing System

The existing carbon credit trading systems predominantly rely on centralized architectures managed by government agencies, international organizations, or designated registries. In these systems:

- **Emission Reporting is Manual:** Industries submit emission reports through paper-based or web-based forms to regulatory authorities. These reports are then manually reviewed and verified by designated auditors, a process that can take several weeks to months.

- **Credit Allocation is Administrative:** Based on verified emission reports, regulatory authorities manually calculate and allocate carbon credits to compliant industries. This process involves significant administrative overhead and is prone to human error.

- **Trading is Intermediary-Dependent:** Carbon credit trading typically occurs through brokers, exchanges, or bilateral agreements, each involving their own fees, settlement timelines, and verification requirements.

- **Record Keeping is Centralized:** All transaction records are maintained in centralized databases managed by registry operators. These databases, while often secure, represent single points of failure and require all participants to trust the registry operator.

- **Price Discovery is Limited:** Market prices are often determined through periodic auctions or over-the-counter negotiations, with limited real-time price discovery mechanisms.

- **No Predictive Analytics:** Existing systems generally do not provide industries with tools to forecast their future emissions, leaving them reactive rather than proactive in their compliance strategies.

### Disadvantages of Existing System

1. Vulnerable to data manipulation and fraud
2. Slow verification and credit allocation processes
3. High transaction costs due to intermediaries
4. Single points of failure in centralized databases
5. Lack of real-time transparency and auditability
6. No integrated emission prediction capabilities
7. Complex and opaque pricing mechanisms
8. No automated penalty and incentive enforcement

## 3.2 Proposed System

The proposed system is a **Blockchain-Enabled Transparent and Tamper-Proof Carbon Credit Trading Platform** that addresses the limitations of existing systems through the integration of three core technologies:

### 3.2.1 Blockchain Layer (Ethereum + Solidity Smart Contracts)

The platform utilizes the Ethereum blockchain to create an immutable, transparent ledger for all carbon credit transactions. A custom Solidity smart contract (`CarbonCredit.sol`) implements an ERC-20 style fungible token called **CarbonCredit (CCT)** with the following capabilities:

- **Token Minting:** Admin-controlled function that creates new CCT tokens when industries report emissions below the baseline. Each token represents 1 ton of CO₂ equivalent reduction.
- **Token Burning:** Any token holder can permanently destroy (burn) their tokens for penalty offset or voluntary carbon retirement.
- **Peer-to-Peer Transfer:** Secure direct token transfers between industry wallets using standard transfer and approval mechanisms.
- **On-Chain Events:** All operations emit blockchain events (Transfer, Approval, Mint, Burn) for complete auditability.

### 3.2.2 AI-Based Prediction Engine

The platform integrates an AI-powered emission prediction model that:

- Aggregates historical emission data for each industry, averaging multiple records per year.
- Calculates the average year-over-year percentage change from historical data.
- Projects future emissions using compound growth formula: `Predicted = Input × (1 + Avg Growth Rate)^Years Ahead`.
- Provides fallback mechanisms (3% default growth rate) when insufficient historical data exists.
- Generates visual trend charts for historical data context.

### 3.2.3 Web Application Layer (Flask + SQLite)

The platform provides a comprehensive web interface built with Flask and features:

- Role-based access control (Admin and Industry roles)
- Industry registration with admin approval workflow
- Emission reporting with document upload and verification
- Carbon credit marketplace with dynamic pricing
- Admin dashboards with analytics and monitoring
- Comprehensive emission analytics pages

## 3.3 Advantages of Proposed System

1. **Tamper-Proof Records:** All transactions are recorded on the Ethereum blockchain, making them immutable and verifiable by any participant.

2. **Automated Credit Allocation:** Smart contracts automatically mint CCT tokens when emission reports demonstrate below-baseline performance, eliminating manual processing delays.

3. **Transparent Marketplace:** A built-in marketplace with supply-demand-based dynamic pricing enables fair and transparent credit trading.

4. **Reduced Intermediaries:** Blockchain-based peer-to-peer trading eliminates the need for brokers and reduces transaction costs.

5. **AI-Powered Prediction:** Integrated emission forecasting helps industries plan their compliance strategies proactively.

6. **Real-Time Monitoring:** Both admin and industry dashboards provide real-time visibility into emission records, credit balances, market prices, and transaction histories.

7. **Automated Penalty System:** Smart contracts automatically assess penalties for non-compliant industries and enable penalty offset through token burning.

8. **Document Verification Workflow:** A structured document review process ensures emission report validity before credit allocation.

9. **Decentralized Trust:** Blockchain eliminates the single-point-of-failure risk and removes the need to trust a central authority.

10. **Scalable Architecture:** The modular design supports easy addition of new features, sectors, and gas types.

## 3.4 Feasibility Study

### 3.4.1 Technical Feasibility

The proposed system is technically feasible as it utilizes well-established and widely adopted technologies:

| Component | Technology | Maturity Level |
|-----------|-----------|---------------|
| Web Framework | Flask (Python) | Production-ready, widely adopted |
| Database | SQLite with SQLAlchemy ORM | Stable, lightweight, suitable for prototype |
| Blockchain | Ethereum (Ganache for development) | Mature, largest smart contract platform |
| Smart Contracts | Solidity v0.8.0 | Stable, well-documented |
| Blockchain Client | Web3.py | Official Python Ethereum library |
| AI/ML | Scikit-learn, NumPy | Industry-standard ML libraries |
| Frontend | HTML5, CSS3, JavaScript | Universal web standards |

All selected technologies have extensive documentation, active community support, and proven track records in production environments. The development team possesses the requisite expertise to implement each component.

### 3.4.2 Economic Feasibility

The project demonstrates strong economic feasibility:

- **Development Costs:** The project uses exclusively open-source technologies (Python, Flask, Solidity, Ganache), eliminating software licensing costs.
- **Infrastructure Costs:** Ganache provides a free local blockchain for development and testing. Deployment to Ethereum testnets is also free.
- **Operational Costs:** The lightweight SQLite database requires minimal server resources. The Flask application can run on modest hardware.
- **Potential Benefits:** Automated verification and trading reduce administrative overhead. Transparent pricing mechanisms improve market efficiency. Reduced intermediary involvement lowers transaction costs.

### 3.4.3 Operational Feasibility

The system is operationally feasible due to:

- **Intuitive User Interface:** The platform features a modern, responsive web interface with clear navigation, informative dashboards, and guided workflows.
- **Role-Based Design:** Separate interfaces for admins and industries ensure that each user type sees only relevant functionality.
- **Minimal Training Requirements:** The web-based interface follows standard interaction patterns, requiring minimal user training.
- **Administrative Control:** The admin has comprehensive tools for managing baselines, verifying documents, approving industries, and monitoring platform activity.

**Table 3.2: Feasibility Study Summary**

| Feasibility Type | Assessment | Key Factors |
|-----------------|-----------|-------------|
| Technical | ✅ Feasible | All technologies are mature, open-source, well-documented |
| Economic | ✅ Feasible | Zero licensing costs, minimal infrastructure requirements |
| Operational | ✅ Feasible | Intuitive UI, role-based access, minimal training required |

---

# CHAPTER 4: PROJECT ARCHITECTURE

## 4.1 Overall System Architecture

The Blockchain-Enabled Carbon Credit Trading Platform follows a **three-tier architecture** that cleanly separates concerns across presentation, application, and data layers. This architectural approach ensures modularity, maintainability, and scalability.

```
┌─────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │  Home    │ │Dashboard │ │ Market   │ │  Prediction  │   │
│  │  Page    │ │  (Admin/ │ │  Place   │ │   Analytics  │   │
│  │         │ │ Industry)│ │         │ │              │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
│  HTML5 / CSS3 / JavaScript / Jinja2 Templates (17 pages)    │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP Requests / Responses
┌─────────────────────────┴───────────────────────────────────┐
│                   APPLICATION LAYER                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Flask Web Application (app.py)          │   │
│  │         39 Route Functions (routes.py)               │   │
│  │    Flask-Login Authentication | Role-Based Access     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌─────────────────┐  ┌─────────────────────────────────┐   │
│  │  AI Prediction  │  │     Blockchain Interface        │   │
│  │    Engine       │  │       (web3_utils.py)           │   │
│  │  (NumPy,       │  │  Web3.py | Contract Interaction  │   │
│  │   Scikit-learn) │  │  Wallet Mgmt | Gas Funding      │   │
│  └─────────────────┘  └─────────────────────────────────┘   │
└─────────────┬──────────────────────────┬────────────────────┘
              │                          │
┌─────────────┴──────────┐  ┌────────────┴────────────────────┐
│       DATA LAYER       │  │      BLOCKCHAIN LAYER           │
│  ┌──────────────────┐  │  │  ┌────────────────────────────┐ │
│  │  SQLite Database │  │  │  │  Ethereum Blockchain       │ │
│  │  (SQLAlchemy ORM)│  │  │  │  (Ganache / Testnet)       │ │
│  │                  │  │  │  │                            │ │
│  │  • User          │  │  │  │  CarbonCredit.sol          │ │
│  │  • Emission      │  │  │  │  (ERC-20 CCT Token)        │ │
│  │  • Baseline      │  │  │  │  • mint()                  │ │
│  │  • MarketOrder   │  │  │  │  • burn()                  │ │
│  │  • MarketConfig  │  │  │  │  • transfer()              │ │
│  │  • CreditRetire  │  │  │  │  • transferFrom()          │ │
│  │  • EmissionDoc   │  │  │  │  • approve()               │ │
│  └──────────────────┘  │  │  └────────────────────────────┘ │
└────────────────────────┘  └─────────────────────────────────┘
```

**Figure 4.1: Overall System Architecture**

### Presentation Layer

The Presentation Layer consists of **17 Jinja2 HTML templates** rendered by the Flask application. The interface features a premium UI design with gradient headers, animated cards, responsive layouts, and interactive charts built with Chart.js. Key pages include:

- `home.html` — Landing page with platform overview
- `register.html` and `login.html` — Authentication pages
- `industry_dashboard.html` — Industry-specific dashboard with credit balances and emission history
- `admin_dashboard.html` — Admin monitoring dashboard with platform-wide analytics
- `report_emission.html` — Emission reporting form with document upload
- `market.html` — Carbon credit marketplace with buy/sell functionality
- `prediction.html` — AI-powered emission prediction interface
- `network.html` — Industry network view with blockchain balances
- `set_baseline.html` — Admin baseline configuration page
- `manage_industries.html` — Industry approval and management
- `industry_emissions_analytics.html` — Detailed emission analytics
- `sell_requests.html` — Trade request management
- `market_config.html` — Dynamic market pricing configuration

### Application Layer

The Application Layer is the core processing engine, built using **Flask (Python)**. Key components include:

- **`app.py`** — Application initialization, database setup, Flask-Login configuration, and default admin account creation.
- **`routes.py`** — Contains 39 route handler functions organized by domain: authentication (4 routes), dashboard (1 route with role-based rendering), emission reporting (1 route), marketplace (4 routes), trading (5 routes), admin management (8 routes), prediction (1 route), analytics (2 routes), and data verification (4 routes).
- **`models.py`** — Defines 7 SQLAlchemy ORM models: `User`, `Baseline`, `Emission`, `MarketConfig`, `MarketOrder`, `CreditRetirement`, and `EmissionDocument`.
- **`web3_utils.py`** — Blockchain interaction module with functions for contract compilation/deployment, wallet creation, token minting/burning/transfer, allowance management, and gas fee management.
- **`extensions.py`** — Shared Flask extension instances (SQLAlchemy, Flask-Login).

### Data Layer

The platform employs a **dual-storage architecture**:

1. **SQLite Database (Relational Data):** Stores user accounts, emission reports, baselines, market orders, market configuration, credit retirements, and uploaded documents. Managed via SQLAlchemy ORM with Flask-Migrate for schema migrations.

2. **Ethereum Blockchain (Immutable Records):** Stores all carbon credit token balances, minting events, burn events, transfers, and approvals as permanent, tamper-proof on-chain records.

This dual-storage approach combines the query flexibility of a relational database with the immutability guarantees of blockchain.

## 4.2 Interaction Between AI, Blockchain, and Web Application

The three core technological pillars of the platform interact in a coordinated manner:

```
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│                  │       │                  │       │                  │
│   WEB APP        │◄─────►│   BLOCKCHAIN     │◄─────►│   AI ENGINE      │
│   (Flask)        │       │   (Ethereum)     │       │   (Scikit-learn) │
│                  │       │                  │       │                  │
│ • User Interface │       │ • CCT Tokens     │       │ • Historical     │
│ • Business Logic │       │ • Smart Contract │       │   Data Analysis  │
│ • Session Mgmt   │       │ • Immutable      │       │ • Compound Growth│
│ • Form Handling  │       │   Ledger         │       │   Projection     │
│                  │       │                  │       │                  │
└────────┬─────────┘       └────────┬─────────┘       └────────┬─────────┘
         │                          │                           │
         │    ┌─────────────────────┴─────────────────────┐    │
         │    │                                           │    │
         └────►        DATA FLOW INTERACTIONS             ◄────┘
              │                                           │
              │ 1. Industry submits emission → Web App    │
              │ 2. Web App checks baseline → Database     │
              │ 3. If below baseline → Mint tokens on BC  │
              │ 4. Industry requests prediction → AI      │
              │ 5. AI reads history → Database            │
              │ 6. AI returns forecast → Web App          │
              │ 7. Trade request → BC executes transfer   │
              │ 8. All tx hashes → stored in Database     │
              └───────────────────────────────────────────┘
```

**Figure 4.4: AI-Blockchain-Web Integration Diagram**

**Key Interaction Flows:**

1. **Emission Reporting → Blockchain Minting:** When an industry submits an emission report through the web interface, the application compares reported emissions against admin-defined baselines. If emissions are below the baseline, the smart contract's `mint()` function is invoked via Web3.py to create CCT tokens in the industry's wallet.

2. **Marketplace Trading → Blockchain Transfer:** When a trade is approved in the marketplace, the smart contract's `transferFrom()` function executes the peer-to-peer token transfer, with the transaction hash recorded in the database.

3. **Penalty Offset → Blockchain Burning:** When an industry offsets penalties, the smart contract's `burn()` function permanently destroys the specified tokens.

4. **AI Prediction → Historical Data:** The AI prediction engine queries historical emission records from the SQLite database, aggregates them by year, calculates growth trends, and projects future emissions.

## 4.3 Smart Contract Workflow

The CarbonCredit smart contract (`CarbonCredit.sol`) is the backbone of the platform's token economy. Written in Solidity v0.8.0, it implements an ERC-20 style token with the following workflow:

```
┌────────────────┐
│  Contract       │
│  Deployment     │
│  (Admin)        │
└───────┬────────┘
        │
        ▼
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│   MINT          │     │   TRANSFER     │     │   BURN         │
│   (Admin Only)  │     │   (Any Holder) │     │   (Any Holder) │
│                 │     │                │     │                │
│ • Credits below │     │ • Direct P2P   │     │ • Penalty      │
│   baseline      │     │   transfer     │     │   Offset       │
│ • New tokens    │     │ • Marketplace  │     │ • Credit       │
│   created       │     │   trades via   │     │   Retirement   │
│ • totalSupply++ │     │   transferFrom │     │ • totalSupply--│
└───────┬────────┘     └───────┬────────┘     └───────┬────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  BLOCKCHAIN EVENTS                           │
│  Transfer | Approval | Mint | Burn                          │
│  (Permanently recorded on Ethereum ledger)                  │
└─────────────────────────────────────────────────────────────┘
```

**Figure 4.3: Smart Contract Interaction Flow**

**Smart Contract Functions:**

| Function | Access | Purpose |
|----------|--------|---------|
| `mint(address to, uint256 amount)` | Admin only | Creates new CCT tokens for compliant industries |
| `burn(uint256 amount)` | Any holder | Permanently destroys tokens for penalty offset or retirement |
| `transfer(address recipient, uint256 amount)` | Any holder | Direct peer-to-peer token transfer |
| `approve(address spender, uint256 amount)` | Any holder | Grants spending allowance to another address |
| `transferFrom(address sender, address recipient, uint256 amount)` | Approved spender | Transfers tokens on behalf of another address (used in marketplace) |
| `balanceOf(address)` | Public view | Returns token balance of an address |
| `allowance(address owner, address spender)` | Public view | Returns approved spending limit |

---

# CHAPTER 5: METHODOLOGY

## 5.1 Step-by-Step Workflow of the System

The platform follows a systematic workflow that encompasses the entire lifecycle of carbon credit management, from industry registration to credit trading and retirement.

### Step 1: Industry Registration and Admin Approval

1. An industry representative navigates to the registration page and provides the company name, owner name, email address, mobile number, and password.
2. The registration request is submitted and stored in the database with `is_approved = False`.
3. The admin reviews pending registration requests on the Manage Industries page.
4. Upon approval, the system automatically generates a unique Ethereum wallet (address + private key) for the industry via `web3_utils.create_wallet()`.
5. The industry can now log in and access the platform.

### Step 2: Admin Sets Emission Baselines

1. The admin navigates to the Set Baseline page.
2. For each combination of **Sector** (e.g., Manufacturing, Energy, Transportation), **Gas Type** (CO₂, CH₄, N₂O), and **Year**, the admin sets an **Allowed Emission** threshold (in tons).
3. These baselines serve as the regulatory cap against which industry emissions are measured.

### Step 3: Industry Submits Emission Report

1. The industry selects the year, sector, gas type, and enters the reported emission amount (in tons).
2. The industry uploads supporting documents (PDF, PNG, JPG, DOC, DOCX, XLSX, CSV) for verification.
3. Documents are stored with unique filenames and linked to the current emission context.
4. The system waits for admin document verification before processing the emission report.

### Step 4: Admin Verifies Documents

1. The admin reviews uploaded documents on the Data Verification page.
2. Documents are organized by industry with pending and total counts displayed.
3. The admin can approve or reject documents individually or in bulk.
4. Once all documents are approved, the emission report proceeds to processing.

### Step 5: Emission Processing and Credit Allocation

1. The system retrieves the applicable baseline for the reported sector, gas type, and year.
2. **If Reported < Baseline (Below Cap):**
   - Credits earned = Baseline − Reported
   - Reduction % = ((Baseline − Reported) / Baseline) × 100
   - The smart contract's `mint()` function creates CCT tokens equal to the credits earned
   - The blockchain transaction hash is recorded in the database
   - Status is set to "Approved"
3. **If Reported ≥ Baseline (Exceeds Cap):**
   - Penalty = Reported − Baseline
   - No tokens are minted
   - Status is set to "Penalty"

### Step 6: Carbon Credit Marketplace Trading

1. **Selling Credits:** Industries with surplus credits create sell listings specifying quantity. Credits are listed at the current dynamic market price.
2. **Buying Credits:** Interested buyers browse available listings and submit purchase requests.
3. **Trade Approval:** The seller reviews incoming buy requests and approves or rejects them.
4. **Blockchain Settlement:** Upon approval, the smart contract executes the token transfer via `transferFrom()`, with the transaction permanently recorded on the blockchain.

### Step 7: Penalty Offset

1. Industries with penalties can offset them by burning CCT tokens.
2. The system validates sufficient token balance before initiating the burn.
3. The smart contract's `burn()` function permanently destroys the tokens.
4. Penalty records are cleared and emission statuses updated to "Approved."

### Step 8: Credit Retirement and Certificate Generation

1. Industries can voluntarily retire credits to prove carbon offset commitments.
2. Retirement burns the tokens on the blockchain permanently.
3. A digital certificate is generated with industry name, credits retired, CO₂ offset, date, and transaction hash.

### Step 9: AI-Powered Emission Prediction

1. Industry enters a target future year and current emission value.
2. The AI engine aggregates historical emission records and calculates growth trends.
3. Future emissions are projected using compound growth formula.
4. Results are displayed along with historical trend visualization.

## 5.2 Data Collection and Validation

Data collection in the platform occurs through multiple channels:

**Industry-Submitted Data:**
- Emission reports containing year, sector, gas type, and reported emission amount
- Supporting documents (certificates, audit reports, measurements) uploaded for admin verification

**Admin-Configured Data:**
- Emission baselines (allowed emission thresholds per sector, gas type, and year)
- Market configuration parameters (base price and adjustment factor)

**Blockchain-Generated Data:**
- Transaction hashes from token minting, burning, and transfers
- On-chain token balances for each industry wallet
- Smart contract event logs (Transfer, Approval, Mint, Burn)

**Data Validation Mechanisms:**

1. **Document Verification:** Admin manually reviews and approves/rejects uploaded emission documents before emission reports are processed.
2. **Baseline Comparison:** Reported emissions are automatically validated against admin-defined baselines to determine credit/penalty status.
3. **Balance Validation:** Token balances are verified on the blockchain before allowing burns, transfers, or trades.
4. **Duplicate Detection:** The system checks for existing emission reports for the same industry, year, sector, and gas type to prevent duplicate submissions.
5. **Input Validation:** Server-side validation ensures all form inputs meet expected formats and ranges.

## 5.3 AI Prediction Process

The AI-based emission prediction follows a structured analytical pipeline:

**Step 1: Data Retrieval**
- Fetch all historical emission records for the current industry from the SQLite database.
- Records include year, sector, gas type, and reported emission amount.

**Step 2: Data Aggregation**
- Group emission records by year.
- For each year, calculate the average reported emission across all records (handling multiple emission types per year).
- Result: A time-series of (year, average_emission) pairs.

**Step 3: Growth Rate Calculation**
- If at least 2 aggregated data points exist:
  - Calculate year-over-year percentage changes: `change = (emission[i] − emission[i−1]) / emission[i−1]`
  - Compute the average growth rate across all consecutive year pairs.
- If fewer than 2 data points exist:
  - Apply a default fallback growth rate of 3% per annum.

**Step 4: Compound Projection**
- Calculate years ahead: `years_ahead = target_year − current_year`
- Apply compound growth: `predicted = input_emission × (1 + avg_growth_rate)^years_ahead`
- Constrain: If predicted value is negative, cap at 0.0.

**Step 5: Visualization**
- Generate historical emission trend data for chart rendering on the frontend using Chart.js.

## 5.4 Smart Contract Automation

The smart contract automation in the platform eliminates manual intervention in critical token operations:

**Automated Minting:**
When an industry submits an approved emission report with emissions below the baseline, the system automatically:
1. Calculates credits earned (baseline − reported emissions)
2. Checks and funds the admin wallet with sufficient ETH for gas
3. Calls `mint_tokens(industry_wallet_address, credits_earned)` via Web3.py
4. Records the returned transaction hash in the Emission record

**Automated Trade Settlement:**
When a seller approves a buy request in the marketplace:
1. The system verifies the seller's token balance and allowance
2. Ensures sufficient gas funding for both parties
3. Executes `transferFrom(seller_address, buyer_address, amount)` via the smart contract
4. Updates order status and records the transaction hash

**Automated Penalty Offset:**
When an industry initiates penalty offset:
1. The system aggregates total penalties from all emission records
2. Validates the industry has sufficient token balance
3. Funds the wallet with gas if needed
4. Executes `burn_tokens(industry_private_key, penalty_amount)`
5. Clears all penalty records and updates emission statuses

## 5.5 Carbon Credit Trading Process

The carbon credit trading process follows a **request-approval model** that ensures both parties consent to every trade:

```
SELLER                          PLATFORM                         BUYER
  │                                │                                │
  │  1. Create Sell Listing        │                                │
  │  (quantity, at market price)   │                                │
  │──────────────────────────────►│                                │
  │                                │  2. Listing visible in market  │
  │                                │──────────────────────────────►│
  │                                │                                │
  │                                │  3. Buy Request submitted      │
  │                                │◄──────────────────────────────│
  │  4. Review buy request         │                                │
  │◄──────────────────────────────│                                │
  │                                │                                │
  │  5a. APPROVE → Blockchain     │                                │
  │      transferFrom() executed   │                                │
  │──────────────────────────────►│  6. Tokens transferred on-chain│
  │                                │──────────────────────────────►│
  │                                │                                │
  │  5b. REJECT → Order cancelled │                                │
  │──────────────────────────────►│                                │
```

**Dynamic Market Price Calculation:**

The market price is dynamically determined using a supply-demand formula:

```
Market Price = Base Price × (1 + Adjustment Factor × (Demand / Supply))
```

Where:
- **Supply (S)** = Total available (unused) credits across all industries
- **Demand (D)** = Total penalty credits required by all non-compliant industries
- **Base Price** = Admin-configured base price (default: ₹500)
- **Adjustment Factor** = Admin-configured sensitivity parameter (default: 0.5)

---

# CHAPTER 6: MODEL

## 6.1 AI Prediction Model Explanation

The AI-based emission prediction module implements a **compound growth projection model** that leverages historical emission data to forecast future industrial emissions. This approach combines time-series analysis with statistical growth modeling to produce realistic, data-driven predictions.

### Model Architecture

The prediction model operates as an analytical pipeline that processes historical data through four stages:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  DATA           │     │  AGGREGATION    │     │  GROWTH RATE    │     │  PROJECTION     │
│  RETRIEVAL      │────►│  ENGINE         │────►│  CALCULATOR     │────►│  ENGINE         │
│                 │     │                 │     │                 │     │                 │
│ • Query DB      │     │ • Group by Year │     │ • YoY % Change  │     │ • Compound      │
│ • Filter by     │     │ • Average per   │     │ • Average Rate  │     │   Growth Formula│
│   Industry      │     │   Year          │     │ • Fallback (3%) │     │ • Non-negative  │
│ • Order by Year │     │ • Sort Timeline │     │                 │     │   Constraint    │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

**Figure 6.1: AI Prediction Model Pipeline**

### Mathematical Foundation

The model is based on the **compound annual growth rate (CAGR)** principle, adapted for emission forecasting:

**Given:**
- Historical emission data: {(y₁, e₁), (y₂, e₂), ..., (yₙ, eₙ)} where yᵢ = year, eᵢ = average emission
- User input: Target year (Y_target) and current emission value (E_current)

**Step 1: Year-over-Year Percentage Change**

For each consecutive pair of years:

```
ΔPct_i = (e_i − e_(i−1)) / e_(i−1)    for i = 2, 3, ..., n
```

**Step 2: Average Growth Rate**

```
r_avg = (1 / (n−1)) × Σ ΔPct_i        for i = 2 to n
```

**Step 3: Compound Projection**

```
E_predicted = E_current × (1 + r_avg)^(Y_target − Y_current)
```

**Step 4: Non-Negative Constraint**

```
E_final = max(E_predicted, 0)
```

## 6.2 Input Parameters

The AI prediction model accepts the following input parameters:

| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| Target Year | Integer | The future year for which emissions are to be predicted | Must be greater than current year |
| Current Emission | Float | The industry's current annual emission in tons | Must be a positive number |
| Historical Records | Auto-retrieved | All past emission records for the industry from database | Aggregated by year |

## 6.3 Prediction Output

The model generates the following outputs:

| Output | Type | Description |
|--------|------|-------------|
| Predicted Emission | Float (2 decimal places) | Forecasted emission for the target year in tons |
| Growth Rate Used | Float | The average annual growth rate applied (historical or default 3%) |
| Historical Trend Data | Array of (year, emission) | Aggregated historical data for chart visualization |
| Prediction Method | String | "Historical growth rate" or "Default 3% growth rate" |

### Interpretation Guide

- **Predicted > Current:** Emissions are expected to increase, suggesting the industry should invest in emission reduction measures.
- **Predicted < Current:** Emissions are expected to decrease, indicating the industry's current reduction efforts are effective.
- **Predicted = 0:** Edge case where negative projections are capped, indicating a near-complete emission elimination scenario (unlikely in practice).

## 6.4 Integration with Blockchain

The AI prediction module integrates with the blockchain layer in the following ways:

1. **Data Source:** The prediction model reads historical emission data from the SQLite database, which includes emission records whose credit allocations have been verified and minted on the blockchain.

2. **Compliance Planning:** Industries use AI predictions to estimate whether they will be below or above future baselines. This helps them decide whether to:
   - Hold their current carbon credits (anticipating future need)
   - Sell surplus credits on the marketplace (if future emissions are projected to decrease)
   - Purchase additional credits proactively (if future emissions are projected to increase)

3. **Blockchain Verification:** While the predictions themselves are not stored on the blockchain (as they are advisory in nature), the historical data that feeds the predictions is backed by blockchain-verified emission records and transaction hashes.

## 6.5 Model Advantages and Limitations

**Advantages:**
- Simple, interpretable model that produces actionable forecasts
- Adapts to each industry's unique historical emission pattern
- Handles data sparsity with intelligent fallback mechanisms
- Non-negative constraint prevents unrealistic predictions
- Real-time computation with no pre-training requirements

**Limitations:**
- Assumes emission trends follow compound growth patterns
- Does not account for external factors (policy changes, technology adoption, economic cycles)
- Accuracy depends on the quality and quantity of historical data
- Limited to univariate prediction (emission amount only)

---

# CHAPTER 7: SOFTWARE DESCRIPTION

## 7.1 Technology Stack Overview

**Table 7.1: Technology Stack Overview**

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Backend Framework | Flask | 2.x | Web application, routing, template rendering |
| Programming Language | Python | 3.8+ | Core application logic |
| Database | SQLite | 3.x | Relational data storage |
| ORM | SQLAlchemy | 1.4+ | Database abstraction and modeling |
| DB Migrations | Flask-Migrate (Alembic) | 4.x | Schema version control |
| Authentication | Flask-Login | 0.6+ | Session-based user authentication |
| Blockchain | Ethereum (Ganache) | - | Decentralized ledger and smart contracts |
| Smart Contracts | Solidity | 0.8.0 | Token contract development |
| Blockchain Client | Web3.py | 6.x | Python-Ethereum interaction |
| Contract Compiler | py-solc-x | 2.x | Solidity compilation from Python |
| AI/ML | Scikit-learn | 1.x | Machine learning algorithms |
| Numerical Computing | NumPy | 1.x | Array operations and mathematics |
| Environment Config | python-dotenv | 1.x | Environment variable management |
| Frontend | HTML5, CSS3, JavaScript | - | User interface |
| Template Engine | Jinja2 | 3.x | Server-side HTML rendering |
| Charting | Chart.js | - | Data visualization |

## 7.2 Python

Python is a high-level, general-purpose programming language known for its readability, versatility, and extensive ecosystem of libraries. In this project, Python serves as the primary programming language for the web application backend, blockchain interaction, AI prediction, and database management.

**Key Features Used:**
- **Dynamic Typing:** Enables rapid prototyping and flexible data handling.
- **Rich Standard Library:** Provides built-in modules for file handling, date/time operations, collections, and more.
- **Package Ecosystem (pip):** Access to thousands of packages via the Python Package Index (PyPI).
- **Object-Oriented Programming:** Used in SQLAlchemy model definitions and Flask application structuring.

**Python Libraries Used in the Project:**

| Library | Purpose |
|---------|---------|
| `flask` | Web application framework |
| `web3` | Ethereum blockchain interaction |
| `py-solc-x` | Solidity smart contract compilation |
| `python-dotenv` | Environment variable management |
| `flask-sqlalchemy` | SQLAlchemy integration with Flask |
| `flask-login` | User session management |
| `flask-migrate` | Database schema migrations |
| `requests` | HTTP requests |
| `scikit-learn` | Machine learning (LinearRegression) |
| `numpy` | Numerical computations |

## 7.3 Flask Framework

Flask is a lightweight, micro web framework for Python based on the WSGI toolkit and Jinja2 template engine. It is designed to be simple, extensible, and easy to learn, making it ideal for both small applications and large-scale deployments.

**Key Flask Components Used:**

1. **Routing:** Flask's decorator-based routing (`@app.route()`) maps URLs to Python functions. The project defines 39 route functions handling all platform functionality.

2. **Template Rendering:** Jinja2 templates enable dynamic HTML generation with Python data. The project uses 17 templates with inheritance from a base template (`base.html`).

3. **Request Handling:** Flask's `request` object provides access to form data, file uploads, session data, and HTTP headers.

4. **Flash Messages:** The `flash()` function displays one-time notification messages to users across page redirects.

5. **Flask-Login Extension:** Manages user sessions, providing `@login_required` decorators and `current_user` proxy for authenticated user access.

6. **Flask-Migrate Extension:** Integrates Alembic database migration framework with Flask, enabling version-controlled schema changes.

**Application Configuration (app.py):**
```python
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carbon_credit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

## 7.4 Web3.py

Web3.py is the official Python library for interacting with the Ethereum blockchain. It provides a comprehensive interface for connecting to Ethereum nodes, deploying smart contracts, sending transactions, and querying blockchain state.

**Key Web3.py Functions Used in the Project:**

| Function | Usage |
|----------|-------|
| `Web3(HTTPProvider(RPC_URL))` | Connect to Ganache blockchain node |
| `web3.eth.account.create()` | Generate new Ethereum wallet for industry |
| `contract.functions.mint()` | Mint new CCT tokens |
| `contract.functions.burn()` | Burn CCT tokens |
| `contract.functions.transfer()` | Direct P2P token transfer |
| `contract.functions.transferFrom()` | Delegated transfer (marketplace) |
| `contract.functions.approve()` | Set spending allowance |
| `contract.functions.balanceOf()` | Query token balance |
| `contract.functions.allowance()` | Query spending allowance |
| `web3.eth.send_raw_transaction()` | Submit signed transactions |
| `web3.eth.get_balance()` | Check ETH balance for gas |
| `web3.eth.chain_id` | Auto-detect blockchain network |

**Transaction Signing Process:**
All blockchain transactions in the platform follow a three-step process:
1. **Build Transaction:** Construct the transaction object with function call, gas limit, gas price, nonce, and chain ID.
2. **Sign Transaction:** Sign the transaction using the sender's private key.
3. **Send and Wait:** Broadcast the signed transaction to the blockchain and wait for the receipt.

## 7.5 Solidity Smart Contracts

Solidity is a statically-typed, contract-oriented programming language designed specifically for implementing smart contracts on the Ethereum Virtual Machine (EVM). The project implements a single smart contract file, `CarbonCredit.sol`, which defines the CCT token.

**Contract Specification:**

```solidity
contract CarbonCredit {
    string public name = "CarbonCredit";
    string public symbol = "CCT";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    address public admin;

    // Events
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Mint(address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);

    // Access Control
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    // Core Functions
    function mint(address to, uint256 amount) external onlyAdmin;
    function burn(uint256 amount) external;
    function transfer(address recipient, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
}
```

**Key Design Decisions:**
- **ERC-20 Compatibility:** The contract follows the ERC-20 token standard interface, ensuring compatibility with Ethereum wallets and tools.
- **Admin-Only Minting:** Only the administrator (contract deployer) can create new tokens, preventing unauthorized credit creation.
- **Public Burning:** Any token holder can burn their own tokens, enabling flexible penalty offset and credit retirement.
- **18 Decimal Places:** Standard Ethereum token precision enabling fractional credit transactions.

## 7.6 Ganache

Ganache is a personal Ethereum blockchain used for development and testing. It provides a simulated blockchain environment with pre-funded accounts, instant mining, and deterministic behavior.

**Configuration in the Project:**
- **RPC URL:** `http://127.0.0.1:7545` (default Ganache port)
- **Pre-funded Accounts:** Ganache provides 10 accounts, each pre-loaded with 100 ETH for gas fees.
- **Instant Mining:** Transactions are immediately mined without waiting for block confirmations.
- **Chain ID:** Automatically detected via `web3.eth.chain_id`.

**Advantages for Development:**
- No real cryptocurrency costs during development and testing
- Instant transaction confirmation for rapid development cycles
- Full control over blockchain state for testing edge cases
- Compatible with standard Ethereum tools and libraries

## 7.7 Frontend Technologies

The platform's frontend is built using standard web technologies enhanced with modern design techniques:

### HTML5
- Semantic HTML elements for accessibility and SEO
- Form elements for user input (registration, emission reporting, trading)
- Table elements for data display (dashboards, analytics)
- File upload inputs for document submission

### CSS3
- Custom CSS stylesheets with modern design aesthetics
- Gradient backgrounds and glassmorphism effects
- Responsive layouts using flexbox and grid
- Smooth animations and transitions for interactive elements
- Premium card-based designs with hover effects

### JavaScript
- Client-side form validation and dynamic interactions
- Chart.js integration for data visualization (supply-demand graphs, emission trends)
- AJAX-style form submissions for seamless user experience
- LocalStorage usage for form data persistence across page refreshes
- Dynamic UI updates based on user interactions

### Jinja2 Template Engine
- Template inheritance with base template (`base.html`) for consistent layout
- Dynamic content rendering with Flask context variables
- Conditional rendering based on user roles (admin vs. industry)
- Loop constructs for rendering data tables and lists

**Table 7.2: Software Requirements**

| Category | Requirement |
|----------|------------|
| Operating System | Windows 10/11, Linux, macOS |
| Python | Version 3.8 or above |
| Node.js | Required for Ganache installation |
| Ganache | Version 7.x or Ganache GUI |
| Web Browser | Chrome, Firefox, Edge (modern version) |
| Code Editor | VS Code, PyCharm, or any IDE |
| Git | Version control (optional) |

**Table 7.3: Hardware Requirements**

| Category | Minimum | Recommended |
|----------|---------|-------------|
| Processor | Intel Core i3 / AMD Ryzen 3 | Intel Core i5 / AMD Ryzen 5 |
| RAM | 4 GB | 8 GB |
| Storage | 500 MB free space | 2 GB free space |
| Network | Internet connection for package installation | Stable broadband |
| Display | 1366 × 768 resolution | 1920 × 1080 resolution |

---
