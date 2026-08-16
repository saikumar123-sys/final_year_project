# Abstract

## Blockchain-Enabled Transparent and Tamper-Proof Carbon Credit Trading Platform with Smart Contract Automation

---

### Overview

Climate change remains one of the most pressing global challenges, with industrial greenhouse gas emissions—including Carbon Dioxide (CO₂), Methane (CH₄), and Nitrous Oxide (N₂O)—being a major contributor. To combat this, governments worldwide have introduced **carbon credit systems** based on the **Cap-and-Trade mechanism**, where industries that emit below a permitted baseline earn tradable credits, while those exceeding the limit must purchase credits to achieve compliance.

However, traditional carbon credit markets are plagued by **data manipulation, fake reporting, lack of transparency, delayed verification, and trust deficits** between participating entities. The proposed platform addresses these challenges by leveraging **Blockchain Technology** and **Smart Contract Automation** to build a **decentralized, transparent, and tamper-proof** carbon credit trading ecosystem. Each carbon credit is tokenized as a digital asset on the Ethereum blockchain, where **1 token = 1 ton of CO₂ equivalent reduction**, and every transaction is permanently recorded on an immutable public ledger, eliminating the possibility of fraud or double-spending.

The platform is built using **Flask (Python)** for the web application layer, **SQLite** for relational data storage, **Solidity** for smart contract development, **Web3.py** for blockchain interaction, and **Scikit-learn/NumPy** for AI-powered emission prediction analytics.

---

### Platform Features

#### 1. User Registration & Authentication

- **Industry Registration**: Industries register with their Industry Name, Owner Name, Email, Mobile Number, and Password. Each registration requires admin approval before accessing the platform.
- **Admin Account**: A default admin account is pre-configured (admin@gmail.com / admin@123), with the ability to change credentials later.
- **Role-Based Access Control**: The system supports two distinct roles—**Admin** (regulatory authority) and **Industry** (participating companies/factories)—with route-level authorization ensuring secure access.
- **Session Management**: Implemented using Flask-Login for persistent, secure user sessions.

#### 2. Blockchain Wallet Management

- **Automatic Wallet Creation**: Upon successful registration approval, each industry is assigned a unique **Ethereum wallet address** and private key, enabling on-chain participation.
- **Gas Fee Management**: The platform automatically monitors wallet ETH balances and funds wallets from the admin account when gas is insufficient for transactions.
- **Wallet Balance Tracking**: Real-time querying of on-chain token balances for each industry wallet.

#### 3. Smart Contract (CarbonCredit Token — CCT)

- **ERC-20 Style Token**: A custom Solidity smart contract (`CarbonCredit.sol`) implements a fungible token named **CarbonCredit (CCT)** with 18 decimals.
- **Minting**: Admin-only function that creates new CCT tokens when industries report emissions below the baseline.
- **Burning**: Any token holder can burn their tokens to permanently retire credits (used for penalty offset and carbon offset certification).
- **Transfer & TransferFrom**: Secure peer-to-peer token transfers with allowance-based delegation for marketplace trading.
- **Approval Mechanism**: Industries approve the admin contract to transfer tokens on their behalf during marketplace transactions.
- **On-Chain Events**: All operations emit blockchain events (Transfer, Approval, Mint, Burn) for auditability.
- **Contract Compilation & Deployment**: Automated Solidity compilation via `py-solc-x` and deployment through the platform's admin interface.

#### 4. Emission Reporting & Management

- **Multi-Field Emission Submission**: Industries submit emission reports specifying Year, Sector, Gas Type, and Reported Emission (in tons).
- **Multiple Emission Types**: An industry can submit multiple emission types (CO₂, CH₄, N₂O) per year, enabling granular tracking.
- **Automatic Baseline Comparison**: Reported emissions are automatically compared against admin-defined baselines for the corresponding sector, gas type, and year.
- **Credit Calculation**: If reported emissions are below the baseline, credits are earned: `Credits = Baseline − Reported`. The reduction percentage is calculated as: `Reduction% = ((Baseline − Reported) / Baseline) × 100`.
- **Penalty Assessment**: If reported emissions exceed the baseline, a penalty is assigned: `Penalty = Reported − Baseline`.
- **Automatic Token Minting**: Upon successful emission submission below the baseline, the smart contract automatically mints the corresponding CCT tokens to the industry's wallet and records the blockchain transaction hash.
- **Document Upload for Verification**: Industries can upload supporting documents (PDF, PNG, JPG, DOC, DOCX, XLSX, CSV) alongside their emission reports for admin verification.
- **Document Lifecycle Management**: Documents are tied to the emission context (year, sector, gas type) and are properly managed across submission cycles.

#### 5. Admin Baseline Management

- **Configurable Emission Baselines**: The admin sets the allowed emission threshold for each combination of sector, gas type, and year.
- **Dynamic Adjustments**: Baselines can be updated at any time, allowing the regulatory authority to tighten or relax caps based on policy requirements.

#### 6. Carbon Credit Marketplace & Trading

- **Sell Credits**: Industries with surplus credits can create sell listings specifying the quantity of credits to sell. Credits are listed at the current dynamic market price.
- **Buy Credits (Request-Based Trading)**: Buyers browse available sell listings and send purchase requests. The seller can then **approve or reject** the trade request.
- **Direct Buy Requests**: Industries can also send direct buy requests to specific industries for a specified number of credits.
- **Blockchain-Settled Trades**: Upon trade approval, the smart contract executes the token transfer from seller to buyer via the `transferFrom` mechanism, with the transaction hash recorded permanently.
- **Trade Status Tracking**: Orders move through lifecycle states: Open → Pending Approval → Completed/Rejected, with full status visibility for both parties.
- **Sell Request Management**: A dedicated tab allows sellers to view, approve, or reject incoming buy requests.

#### 7. Dynamic Market Price Engine

- **Supply-Demand Based Pricing**: The market price of carbon credits is dynamically calculated using:
  - **Supply (S)** = Total available (unused) credits across all industries
  - **Demand (D)** = Total penalty credits required by all non-compliant industries
  - **Formula**: `Market Price = Base Price × (1 + Adjustment Factor × (D / S))`
- **Admin-Configurable Parameters**: The admin controls the **Base Price** and **Adjustment Factor**, allowing fine-tuned market regulation.
- **Real-Time Pricing**: Market price updates dynamically as emissions are reported and credits are traded.

#### 8. Penalty Offset Mechanism

- **Automatic Penalty Aggregation**: Total penalties are aggregated from all emission records for each industry.
- **Token Burning for Compliance**: Industries can offset their penalty by burning the equivalent CCT tokens from their wallet via the smart contract's `burn` function.
- **Balance Validation**: The system validates that the industry has sufficient token balance before initiating a burn operation.
- **Gas Funding Check**: Before executing the burn, the platform ensures the wallet has enough ETH for gas fees, auto-funding if necessary.
- **Post-Offset Status Update**: Upon successful offset, all penalty records are cleared and emission statuses are updated to "Approved."

#### 9. Credit Retirement & Carbon Offset Certificates

- **Permanent Credit Retirement**: Industries can retire credits to prove carbon offset, which permanently burns the tokens on the blockchain.
- **Certificate Generation**: After retirement, the system generates a digital certificate containing Industry Name, Credits Retired, CO₂ Offset Amount, Date, and Blockchain Transaction Hash.
- **Anti-Fraud Protection**: Retired credits cannot be reused or re-traded, ensuring environmental integrity.

#### 10. AI-Powered Emission Prediction

- **Future Emission Forecasting**: Industries can predict their future emissions by entering a target year and current emission value.
- **Historical Data Aggregation**: The system aggregates historical emission records, averaging multiple entries per year, to derive meaningful trends.
- **Compound Growth Projection**: Uses the average year-over-year percentage change from historical data to forecast emissions using the compound growth formula: `Predicted = Input × (1 + Avg Growth Rate) ^ Years Ahead`.
- **Fallback Mechanism**: When insufficient historical data exists (fewer than 2 data points), a default 3% annual growth rate is applied.
- **Non-Negative Constraint**: Predictions are constrained to never produce negative emission values.
- **Historical Trend Visualization**: The prediction page includes a chart displaying aggregated historical emissions for visual context.

#### 11. Data Verification System (Admin)

- **Document Review Workflow**: Admin can view all uploaded emission documents organized by industry, with pending and total document counts displayed.
- **Approve/Reject Documents**: Admin can individually approve or reject uploaded documents, recording the review timestamp.
- **Bulk Verification**: Admin can approve or reject all pending documents for an industry at once.
- **Status Tracking**: Documents progress through states: PENDING VERIFICATION → APPROVED / REJECTED.

#### 12. Industry Management (Admin)

- **Industry Approval/Rejection**: Admin reviews and approves or rejects new industry registration requests.
- **Account Suspension**: Admin can suspend suspicious industry accounts, preventing them from accessing the platform.
- **Emission History Viewing**: Admin can view the complete emission history of any registered industry.
- **Penalty Status Monitoring**: Admin has visibility into penalty statuses across all industries.

#### 13. Industry Network View

- **Registered Industries Overview**: Industries can view all other registered industries on the platform.
- **Real-Time Blockchain Balances**: The network page displays live token balances queried directly from the blockchain for each industry.
- **Trading Partner Discovery**: Enables industries to identify potential trading partners based on available credit balances.

#### 14. Dashboards & Analytics

##### Industry Dashboard
- Total registered industries count
- Available credits (real-time blockchain balance)
- Total penalty amount
- Transaction count (completed trades)
- Current market price display
- Emission history with tabular data (Industry ID, Sector, Year, Gas Type, Reported Emissions, Baseline, Reduction %, Credits Gained)

##### Admin Dashboard
- Total registered industries count
- Total credits issued across the platform
- Total credits traded (completed transactions)
- Total penalty industries count
- Current market price (dynamically calculated)
- Supply vs. Demand visualization graph

##### Emission Analytics Page
- Total emissions aggregated
- Emission types breakdown
- Average reduction percentage
- Data points count (total emission records)
- Detailed emission records table

#### 15. Blockchain Ledger & Transaction Transparency

- **Immutable Transaction Records**: Every credit minting, transfer, burn, and trade is recorded on the Ethereum blockchain with a unique transaction hash.
- **Public Auditability**: All blockchain transactions are verifiable through the transaction hashes stored in the database and displayed throughout the platform.
- **Tamper-Proof Assurance**: Once recorded, no blockchain entry can be altered or deleted.

#### 16. Data Synchronization & Integrity

- **Blockchain-Database Reconciliation**: A dedicated synchronization script (`sync_data.py`) reconciles database records with actual on-chain token balances.
- **Automatic Deficit Minting**: If on-chain balance is lower than expected (based on earned, bought, sold, and retired credits), the system mints the difference to restore consistency.
- **Allowance Repair**: Ensures all industries with open sell orders have sufficient token allowance approved for the admin to execute trades.

#### 17. Security Features

- **Immutable Blockchain Ledger**: All critical operations are permanently recorded on-chain.
- **Password Hashing**: User passwords are hashed using Werkzeug's security utilities.
- **Role-Based Authorization**: Every route is protected by role checks (admin vs. industry).
- **Ownership Verification**: Token ownership is verified via blockchain wallet addresses.
- **Double-Spending Prevention**: Smart contract logic ensures tokens cannot be spent twice.
- **Transparent Audit Trail**: Complete transaction history enables fraud detection.

---

### Technology Stack

| Layer | Technology |
|---|---|
| **Web Framework** | Flask (Python) |
| **Database** | SQLite with SQLAlchemy ORM |
| **Database Migrations** | Flask-Migrate (Alembic) |
| **Authentication** | Flask-Login with session management |
| **Blockchain** | Ethereum (Ganache/Testnet) |
| **Smart Contract Language** | Solidity (v0.8.0) |
| **Blockchain Interaction** | Web3.py |
| **Contract Compilation** | py-solc-x |
| **AI/ML Prediction** | Scikit-learn, NumPy |
| **Environment Config** | python-dotenv |
| **Frontend** | HTML5, CSS3, JavaScript (Jinja2 templates) |

---

### System Architecture

The platform follows a **three-tier architecture**:

1. **Presentation Layer**: 17 Jinja2 HTML templates with premium UI design featuring gradient headers, animated cards, responsive layouts, and interactive charts.
2. **Application Layer**: Flask-based backend with 39 route functions handling authentication, emission reporting, marketplace trading, admin operations, prediction analytics, and data verification.
3. **Data Layer**: Dual-storage approach—SQLite database for relational data (users, emissions, orders, configurations) and Ethereum blockchain for immutable credit tokenization and transaction records.

---

### Conclusion

The Blockchain-Enabled Carbon Credit Trading Platform provides a comprehensive, secure, and transparent solution for managing industrial carbon emissions. By integrating blockchain-based smart contract automation with intelligent emission prediction analytics and a dynamic marketplace, the platform ensures tamper-proof compliance tracking, fair credit trading, and verifiable environmental accountability. The system promotes responsible industrial behavior while enabling an efficient and trustworthy carbon credit ecosystem.

---
