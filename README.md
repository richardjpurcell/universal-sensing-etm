# Universal Sensing ETM (USETM)

The **Universal Sensing ETM (USETM)** project provides a modular, object-oriented framework for integrating multi-modal sensor data into an Extended Turing Machine (ETM) and Universal Sensor Encoding environment. By using a universal encoding function, hierarchical encoding, and state-aware precision control, this system demonstrates the advantages of ETM-based sensor processing over traditional non-ETM methods.

## Overview

This framework:
- Extends the classical Turing machine concept to handle multiple sensor inputs.
- Encodes continuous or complex sensor signals into discrete symbolic streams.
- Dynamically adjusts precision and resolution based on data variability (entropy) and contextual importance.
- Compares ETM-based sensor computation against systems that do not employ these extended concepts.

## Key Components

- **Sensors**:  
  Represented by `Sensor` objects, each responsible for handling data from one type of sensor input (e.g., temperature, wind).
  
- **Data Handling**:  
  The `DataLoader` class loads raw NetCDF files and converts them into DataFrames.  
  The `DataPreprocessor` class cleans and normalizes the data before encoding.
  
- **Encoding**:  
  The `UniversalEncoder` and optional `HierarchicalEncoder` classes transform raw sensor data into a unified symbolic format suitable for ETM processing.
  
- **Extended Turing Machine (ETM)**:  
  The `ExtendedTuringMachine` class simulates the ETM, processing encoded data streams, managing states, and adapting encoding precision as needed.
  
- **State-Aware Precision Control & Entropy Estimation**:  
  The `StateAwarePrecisionController` and `EntropyEstimator` classes monitor data variability, instructing the ETM and encoders to increase or decrease resolution dynamically.
  
- **Comparison Framework**:  
  The `ETMComparisonFramework` class provides a way to run experiments, comparing ETM-based solutions against non-ETM approaches in terms of performance, resource usage, and accuracy.

