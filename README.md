# Real Time Stock Analytics API

A production grade real time stock analytics platform built with FastAPI and Azure based streaming and analytics services.

This project will ingest live and historical stock market data for the five largest global companies, process it using Azure Fabric streaming and Spark based analytics, and expose clean analytical APIs for real time insights.

The goal is to demonstrate backend engineering, data engineering, and analytics engineering skills in one evolving system.

---

## Project Status

This project is currently in the design and foundation phase.

All architecture, data flow, and development phases are being built incrementally.

---

## Why This Project Exists

This project is being built to demonstrate real world capability in:

• API design with FastAPI  
• Cloud based real time data ingestion  
• Streaming analytics using Azure Fabric  
• Analytical data modelling  
• Scalable system architecture  
• Production ready testing and deployments  

This is a portfolio grade engineering platform.

---

## Initial Scope

The API will focus on:

• Live stock prices  
• Historical price data  
• Rolling averages  
• Daily high and low values  
• Volume based analytics  
• Volatility calculations  

---

## Tracked Companies

The platform will track data for:

• Apple  
• Microsoft  
• Amazon  
• Google  
• Nvidia  

These companies were selected due to free public data availability and strong industry relevance.

---

## Planned High Level Flow

External Stock APIs  
→ Python Producer  
→ Azure Event Ingestion  
→ Azure Fabric Eventstream  
→ Streaming Analytics via KQL or Spark Structured Streaming  
→ Fabric Warehouse or Lakehouse  
→ FastAPI Analytics API  

All real time processing and rolling calculations will be handled inside Azure to reduce local infrastructure requirements.

---

## Planned Technology Stack

This section reflects the intended stack and will be updated only when tools are actively used in code.

• Python  
• FastAPI  
• Microsoft SQL
• Azure Event Hubs or Fabric Eventstream  
• Azure Fabric Spark Structured Streaming or KQL  
• Redis for caching  
• Docker  
• GitHub Actions  
• Azure  

---

## Planned API Endpoints

The endpoints will be added progressively once Phase 1 begins.

---

## Data Engineering Focus

This platform is designed to showcase:

• External API ingestion  
• Cloud based streaming pipelines  
• Time window analytics  
• Analytical schema design  
• API layers above real time analytical storage  
• Caching strategies for performance  

---

## Development Roadmap

Phase 1  
FastAPI foundation, database modelling, historical endpoints  

Phase 2  
Azure based real time ingestion through Eventstream  

Phase 3  
Rolling analytics using Spark Structured Streaming or KQL  

Phase 4  
Caching, performance tuning, and reliability improvements  

Phase 5  
Cloud deployment and dashboard integration  

---

## Disclaimer

This project is not meant for any real financial decisions.

