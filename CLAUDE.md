# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based electrical transmission system valuation project that processes and analyzes transmission component data for 2024-2027 period. The system uses Prefect for workflow orchestration and supports both PostgreSQL and MariaDB databases.

## Documentation Guidelines

### Language Requirements for Documentation

**IMPORTANT**: All documentation in the `docs/` folder must be written in **Spanish** as it is intended for final users (not developers). The documentation should be:

- **In Spanish**: Use proper Spanish terminology and grammar throughout
- **Detailed and User-Focused**: Written for system operators and business users, not programmers
- **Step-by-Step**: Include clear, sequential instructions for all processes
- **Comprehensive**: Cover all use cases, error scenarios, and expected outputs
- **Visual**: Include examples of commands, expected outputs, and data structures where helpful

Examples of user documentation that should be in Spanish:
- Validation guides (`docs/validacion_*.md`)
- Process documentation (`docs/arquitectura.md`, `docs/metodos.md`)
- Data source documentation (`docs/origenes de datos.md`)
- User manuals and operation guides

Note: Code comments, docstrings, and technical developer documentation (like this CLAUDE.md file) remain in English.

### Documentation Formatting

**IMPORTANT**: When writing or updating documentation in the `docs/` folder:

- **Do NOT include line numbers**: Documentation should be clean and readable without line numbers
- Line numbers make documentation harder to maintain as they need to be updated with every edit
- Focus on clear section headings, bullet points, and code blocks without line number references
- When referring to code, use descriptive names and file paths instead of line numbers

### Documentation Content Focus

**IMPORTANT**: Documentation should focus on **functionality** (what the system does), not **implementation details** (how it's built):

**Write about:**
- ✅ What each function/feature does
- ✅ What inputs it accepts and outputs it produces
- ✅ When and why to use it
- ✅ Usage examples with expected results
- ✅ Business logic and classification rules
- ✅ Data sources and formats

**Do NOT write about:**
- ❌ Caching mechanisms and performance optimizations
- ❌ Internal data structures (dictionaries, tuples, etc.)
- ❌ Algorithm complexity (O(1), O(n), etc.)
- ❌ Module-level variables and implementation patterns
- ❌ Memory management techniques

**Example - Good (Functionality-focused):**
> "Clasifica conductores según su descripción técnica mediante búsqueda en base de datos. Lee clasificaciones desde `input/conductores.xlsx` y valida que todos los conductores tengan una clasificación definida."

**Example - Bad (Implementation-focused):**
> "Uses module-level cache dictionary for O(1) lookup performance. Loads all classifications into `_conductor_classification_cache` on first invocation using lazy initialization pattern."

## Library Requirements

### Multiplatform Compatibility

**CRITICAL**: All libraries added to this project must be multiplatform compatible and work reliably on:
- **Windows** (Windows 10/11)
- **Linux** (Ubuntu/CentOS/Debian distributions)
- **macOS** (Intel and Apple Silicon)

When selecting dependencies:
- Prefer pure Python libraries when possible
- Avoid platform-specific compiled dependencies
- Test on multiple platforms before adding to requirements
- Choose libraries with active maintenance and cross-platform CI/CD
- Document any platform-specific installation requirements

This ensures the project can be deployed and developed consistently across different operating systems and environments.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3.13 -m venv .venv
source .venv/bin/activate
```

### Database Setup

This deletes the existing database and creates a new one with the required schema. Apply this after doing changes to the database schema or when starting fresh.
```bash
python -m scripts.setup
```

### Running the Workflow

This command runs the Prefect workflow, which orchestrates the ETL process and report generation. It takes a couple of hours to run.
```bash
python -m scripts.workflow
```

### Testing and Code Quality
```bash
# Install and run pre-commit hooks
pip install pre-commit
pre-commit install
pre-commit run --all-files

# Run tests with coverage
make test
```

### Code Formatting
The project uses:
- **Black** for code formatting (88 character line length)
- **isort** for import sorting (black profile)
- **flake8** for linting
- **mypy** for type checking

## Architecture

### Core Components
- **Prefect Workflows**: Orchestrates ETL processes with parallel execution
- **Dynamic Query Builder**: Constructs SQL queries based on table dependencies
- **Dual Database System**: PostgreSQL for initial data loading, MariaDB for processing
- **Report Generation**: Excel-based output with audit trails and MariaDB integration

### Package Structure
- `scripts/load/`: Database loading and migration utilities
- `scripts/reports/`: Report generation and data export
- `scripts/models/`: Data model definitions (calificacion, decreto, familia_grupo, etc.)
- `scripts/utils/`: Shared utilities (database, Excel, file operations)
- `scripts/validaciones/`: Data validation modules
- `config/`: Configuration and settings
- `tests/`: Test suite
- `input/`: Input data files (calificacion, familias_objetos.json, parametros.json)
- `output/`: Generated reports organized by type

### Data Flow
1. Load SQL dump into PostgreSQL
2. Extract schema and migrate to MariaDB
3. Process data using Prefect workflows with parallel transformations
4. Generate Excel reports and validation files
5. Export results and audit information
6. Store report data in MariaDB for querying

## Key Features

### Dynamic Query Construction
The system automatically builds SQL queries with JOINs based on foreign key relationships defined in `table_relationships.py`. Uses dependency trees to construct complex queries that follow table hierarchies (e.g., `pano -> patiosubestacion -> subestacion`).

### Parallel Processing with Prefect
Transformations run in parallel for each table using `@task` decorators. The main workflow (`scripts/workflow.py`) coordinates parallel execution with proper dependency management and caching.

### Tension Value Resolution
Complex logic in `compute_objetos.py:get_tension()` that searches for voltage values across multiple datasheet prefixes. Handles primary/secondary/tertiary voltages for transformers and fallback logic for equipment like panos that inherit tension from parent components.

### Report Output Management
- **Excel/CSV Export**: `write_excel_output()` automatically switches to CSV for large datasets (>1M rows)
- **MariaDB Integration**: Reports with `output_type="resultados_generales"` are automatically stored in MariaDB with `_reporte_` prefix
- **Organized Output Structure**:
  - `resultados_generales/`: Final reports for end users
  - `resultados_por_tabla/`: Detailed table-by-table analysis
  - `validacion/`: Data validation reports
  - `componentes_calificados/`: Component qualification status

### Generic Component Processing
The architecture supports processing different types of electrical components through:
- **Family-Object Mapping**: `familias_objetos.json` defines component hierarchies
- **Dynamic Datasheet Expansion**: Automatically expands JSON datasheet fields into tabular columns
- **Parameter Collection**: Generic parameter extraction from `parametro1-20` columns with normalization
- **Type Element Inference**: Automatic detection of component types from datasheet content

### Data Models and Business Logic
- **Calificacion System**: Complex voltage level and geographic zone classification
- **NUP Integration**: Links to transmission project database with valorization flags
- **Technical Data Resolution**: Handles references to external technical specifications
- **Status Management**: Tracks component operational status with validation rules

## Common Patterns

### Error Handling and Validation
- Type checking with mypy for static analysis
- Pandas NA handling for missing data
- Database connection pooling with retry logic
- Comprehensive validation reports for data quality

### Performance Optimization
- Prefect caching to avoid recomputation
- Database connection pooling
- Memory management with explicit garbage collection
- Chunked database operations for large datasets

### Testing Strategy
- Component-specific test files (e.g., `test_torres.py`, `test_transformadores.py`)
- Mock data generation for isolated testing
- Database integration tests
- Report output validation

## Troubleshooting

### Common Issues and Solutions

#### Environment Setup
**Always activate the virtual environment before running Python commands:**
```bash
source .venv/bin/activate
```

#### Tension Value Issues
**Problem**: `tension1` column showing null when tension data exists in related tables
- **Root Cause**: `get_tension()` function incorrectly identifying pandas `<NA>` as valid data
- **Solution**: Check for both `is not None` and `pd.notna()` when determining if main object has tension data
- **Location**: `scripts/reports/compute_objetos.py:153-156`

**Problem**: Missing `tension2` and `tension3` values for transformers
- **Root Cause**: Early break logic stopping search after finding `tension1`
- **Solution**: Remove premature break conditions, continue searching for all tension types
- **Location**: `scripts/reports/compute_objetos.py:174-184`

#### Type Checking Errors
**Problem**: mypy errors about incompatible assignment types
- **Solution**: Use proper type annotations (`dict[str, Any]`) and type guards for arithmetic operations
- **Example**: Check `isinstance(value, (int, float))` before arithmetic operations

#### Report Column Ordering
**Problem**: Mixed column ordering in reports (tension1, potencia1, tension2, etc.)
- **Solution**: Use ordered dictionaries to ensure logical grouping of related columns
- **Location**: `scripts/reports/reporte_instalacion_familia.py:calculate_group_summary()`

#### Database Connection Issues
**Problem**: Connection timeouts or pool exhaustion
- **Solution**: Use connection pooling with proper cleanup and retry logic
- **Configuration**: `scripts/utils/db_utils.py` connection settings

### Development Tips

#### Running Single Table Processing
```bash
# Test specific table processing
python -c "
from scripts.reports.compute_objetos import calcular_single_table
calcular_single_table('pano')
"
```

#### Debugging Tension Logic
Add debug prints in `get_tension()` function to trace value resolution:
```python
if table_name == "target_table" and row["id_objeto"] == target_id:
    print(f"DEBUG: Found {datasheet_key} = {row[datasheet_key]}")
```

#### Database Schema Changes
After modifying database schema or data models:
1. Update migration scripts in `scripts/load/`
2. Run `python -m scripts.setup` to rebuild database
3. Update corresponding test files
4. Run full workflow to verify changes

## Git and PR Management

### Commit Process
- Always commit changes after significant modifications
- Never skip commit hooks - they ensure code quality
- Use descriptive commit messages that explain the "why" not just the "what"
- Follow the established commit message format in the repository

### Pull Request Management
- Update PR titles to reflect comprehensive changes when multiple features are involved
- Include detailed summaries of all changes in PR descriptions
- Mark test plan items as completed after verification
- Push changes regularly to keep PRs up to date

### Database Table Management
When renaming database tables:
1. **Table Rename Pattern**: Use descriptive names (e.g., `_calificacion_componentes` → `_informacion_stx`)
2. **Code Updates**: Search and replace all references across Python files
3. **Migration Strategy**: Update schema creation scripts in `scripts/load/`
4. **Report Integration**: Verify MariaDB report table names are updated correctly

### Data Quality and Filtering
- **Quantity Validation**: Filter out objects with `cantidad = false` or null quantities
- **Component Processing**: Remove unnecessary fields like `antecedentesComplementarios` from tipo elemento
- **Unit Conversion**: Ensure proper unit normalization (e.g., hectáreas to m²)

### Report Generation Improvements
- **Cache Management**: Update `workflow_cache.py` when modifying workflow steps
- **Report Cleanup**: Remove internal reports that are no longer needed
- **Output Organization**: Maintain clear separation between user-facing and internal reports

### Testing and Validation
After major changes, verify:
1. Database schema recreates correctly with `python -m scripts.setup`
2. Full workflow completes without errors with `python -m scripts.workflow`
3. All reports generate successfully
4. Unit conversions work correctly
5. Data filtering operates as expected
6. Pre-commit hooks pass all checks

## Development Workflow and Git Management

### Pre-commit Hooks Setup
The project uses pre-commit hooks to maintain code quality. If you encounter pre-commit hook issues:

1. **Ensure virtual environment is activated**: Pre-commit hooks require the development dependencies to be available
   ```bash
   source .venv/bin/activate
   ```

2. **Install pre-commit if not already installed**:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

3. **Common Pre-commit Issues**:
   - **flake8 not found**: Always run git commands from within the activated virtual environment
   - **JSON syntax errors in parametros.json**: Fix trailing commas and missing commas after `"componente": true` fields
   - **Unused imports**: Remove unused import statements (e.g., `import pytest` when not used)

### Git Branch and Commit Workflow
1. **Always create feature branches**: Never commit directly to mainline
   ```bash
   git checkout -b feat/descriptive-feature-name
   ```

2. **Commit with activated environment**: Ensures pre-commit hooks can find all tools
   ```bash
   source .venv/bin/activate
   git add files...
   git commit -m "descriptive message"
   ```

3. **Push and create PR**: Use GitHub CLI for consistent PR creation
   ```bash
   git push -u origin feat/feature-name
   gh pr create --title "title" --body "description"
   ```

### Component System Development

#### Component Parameter Types
The component system supports two types of component parameters in `parametros.json`:

1. **Regular components**: `"componente": true` - Uses raw parameter values
2. **Tension components**: `"componente": "tension"` - Applies voltage classification:
   - **BT** (Baja Tensión): < 10 kV
   - **MT** (Media Tensión): 10-68.99 kV
   - **AT** (Alta Tensión): 69-153.99 kV
   - **EAT** (Extra Alta Tensión): ≥ 154 kV

#### Component Generation Strategy
The system generates components based on **existing combinations** in the database, not theoretical possibilities:

- **Single parameter**: Queries unique values for that parameter
- **Multiple parameters**: Queries existing combinations across all parameters
- **Tension classification**: Applied during processing to group similar voltage levels

#### Current Component Statistics
As of the latest implementation:
- **reactor**: 11 components (tension + tipoFase + tipoReactor combinations)
- **rellenoCompactado**: 14 components (tipoSuelo + tipoRellenoCompactado combinations)
- **excavacion**: 7 components (single tipoSuelo parameter)
- **transformador2d**: 4 components (tension classifications: BT, MT, AT, EAT)
- **condensadorserie**: 1 component
- **pararrayo**: 4 components

#### Adding Component Support to New Tipo Elementos
When adding component support to new parameters in `parametros.json`:

1. **Update parametros.json**: Add `"componente": true` or `"componente": "tension"` to relevant parameter definitions
2. **Test with build_componentes**: Verify the function works with your new tipo_elemento
   ```bash
   python -c "
   from scripts.montaje.componentes import build_componentes
   result = build_componentes('your_tipo_elemento')
   print(f'Generated {len(result)} components')
   for comp in result[:3]:  # Show first 3
       print(f'  {comp[\"name\"]}: {comp}')
   "
   ```
3. **Add tests**: Create test cases for your new component type in `tests/test_componentes.py`
4. **Verify realistic counts**: Components should reflect actual data combinations, not theoretical maximums

#### Database Column Mapping
The component system uses this mapping pattern:
- `parametroX` in parametros.json → `valor_paramX` and `nombre_paramX` in `_informacion_stx` table
- Always verify the database has the expected columns and data before adding component support
- For multi-parameter components, ensure all parameter combinations exist in the data

#### Implementation Details
- **File**: `scripts/montaje/componentes.py`
- **Main function**: `build_componentes(tipo_elemento: str)`
- **Generation**: `generate_all_componentes()` creates Excel output for all supported tipo_elementos
- **Output**: `output/interno_validacion/componentes_tipo.xlsx`
- **Testing**: `tests/test_componentes.py` contains comprehensive test coverage
