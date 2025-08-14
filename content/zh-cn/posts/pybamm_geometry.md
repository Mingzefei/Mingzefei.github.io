# PyBaMM 几何 (Geometry) 模块详解

PyBaMM 中的几何模块 (`src/pybamm/geometry/`) 负责定义模型方程求解的空间区域（计算域）及其相关的坐标系统。它是连接符号模型与数值离散化的关键环节，为后续的网格生成和空间算子离散化提供基础。

## 1. 几何模块的核心作用

几何模块在 PyBaMM 中的核心作用包括：

*   **定义计算域 (Computational Domain):** 明确模型中各个物理过程发生的空间范围。例如，在电池模型中，这些域通常包括负极、隔膜、正极、以及可能的集流体区域。对于包含颗粒相的模型，还会定义颗粒内部的微观域。
*   **指定坐标系 (Coordinate Systems):** 为每个域指定相应的空间坐标变量（如宏观的 `x` 坐标，颗粒内部的 `r` 坐标）及其取值范围。这些坐标通常是标准化的，并在参数化后映射到实际的物理尺寸。
*   **支持离散化 (Support for Discretisation):** 提供构建网格 (Mesh) 所需的几何信息。离散化模块 (`pybamm.Discretisation`) 会依据几何对象来生成网格，并将模型中的空间微分算子（如梯度、散度）转换为数值形式（如有限差分矩阵）。
*   **参数化 (Parameterisation):** 几何尺寸（如电极厚度 `L_n`, `L_s`, `L_p`，颗粒半径 `R_n`, `R_p`）在模型中通常表示为符号参数。通过 `pybamm.ParameterValues` 对象赋予这些参数具体数值后，几何模块才能确定最终的坐标范围和边界位置。
*   **核心类 `pybamm.Geometry`:** 这是几何模块的中心类，用于存储和管理所有域的几何信息。它通常在模型设置完成后，传递给 `Discretisation` 对象进行处理。

## 2. 域 (Domain) 与子域 (Sub-domain)

在 PyBaMM 中，物理域和子域通常用字符串来标识，这些是模型中变量和方程定义的基础。

*   **Domain (域):** 指的是模型中主要的、宏观的物理区域。常见的域包括：
    *   `"negative electrode"`
    *   `"separator"`
    *   `"positive electrode"`
    *   `"current collector"` (在考虑集流体效应时使用，可以是1D、2D或3D)

*   **Sub-domain (子域):** 通常指嵌入在主域内的微观尺度域。最常见的例子是多孔电极中的活性材料颗粒：
    *   `"negative particle"` (描述负极活性材料颗粒内部)
    *   `"positive particle"` (描述正极活性材料颗粒内部)
    这些子域有其自身的坐标系统（如颗粒半径 `r`）。

模型在定义变量时会指定其所在的域，例如：
`c_e = pybamm.Variable("Electrolyte concentration", domain=["negative electrode", "separator", "positive electrode"])`
`c_s_n = pybamm.Variable("Negative particle concentration", domain="negative particle", auxiliary_domains={"secondary": "negative electrode"})`
(这里的 `auxiliary_domains` 用于指明子域 `negative particle` 是在宏观域 `negative electrode` 中分布的。)

## 3. 坐标系 (Coordinate Systems)

PyBaMM 使用标准化的空间变量，这些变量在 `src/pybamm/geometry/standard_spatial_vars.py` 中定义。

*   **`x` (宏观坐标):** 通常表示沿着电芯厚度方向的一维坐标。
    *   `x_n`: 负极内的坐标 (通常从 0 到 1，对应物理尺寸 0 到 `L_n`)。
    *   `x_s`: 隔膜内的坐标 (通常从 0 到 1，对应物理尺寸 `L_n` 到 `L_n + L_s`)。
    *   `x_p`: 正极内的坐标 (通常从 0 到 1，对应物理尺寸 `L_n + L_s` 到 `L_n + L_s + L_p`)。
    *   `x_cc`: 集流体内的坐标。
*   **`r` (微观坐标):** 通常表示球形活性材料颗粒内部的径向坐标。
    *   `r_n`: 负极颗粒内的径向坐标 (通常从 0 到 1，对应物理尺寸 0 到 `R_n`)。
    *   `r_p`: 正极颗粒内的径向坐标 (通常从 0 到 1，对应物理尺寸 0 到 `R_p`)。
*   **`R` (颗粒半径参数):** 注意 `R_n` 和 `R_p` 通常指颗粒的半径，它们是几何参数，而不是坐标变量。
*   **`y`, `z` (平面坐标):** 用于描述二维或三维集流体模型中的平面坐标。

`pybamm.Geometry` 对象负责将这些抽象的域名（如 `"negative electrode"`）映射到具体的空间坐标变量（如 `pybamm.standard_spatial_vars.x_n`）及其经过参数化后的数值范围。

## 4. `pybamm.Geometry` 类

*   **定义与使用:**
    *   `pybamm.Geometry` 类 (定义于 `src/pybamm/geometry/geometry.py`) 是几何信息的核心容器。
    *   它通常通过一个字典来初始化，该字典的键是域名，值是包含该域详细信息的字典（例如，该域关联的空间变量、坐标范围、边界等）。
    *   PyBaMM 提供了预定义的几何构建函数，如 `pybamm.battery_geometry()` (定义于 `src/pybamm/geometry/battery_geometry.py`)。这个函数可以根据模型选项（如维度 "1D", "2D current collector", "particle phase" 等）和已处理的参数自动生成常用的电池几何结构。用户也可以根据需求构建自定义的几何对象。

*   **结构示例:**
    一个典型的 `Geometry` 对象内部可能如下所示（简化）：
    ```python
    {
        "negative electrode": {
            "primary": pybamm.standard_spatial_vars.x_n,
            "min": pybamm.Scalar(0),
            "max": param.n.L,  # L_n after processing
            "tabs": {"negative": "left", "positive": "right"} # Example for current collector
        },
        "separator": {
            "primary": pybamm.standard_spatial_vars.x_s,
            "min": param.n.L,
            "max": param.n.L + param.s.L
        },
        # ... other domains like positive electrode, particles ...
    }
    ```

## 5. 几何参数 (`GeometricParameters`)

几何参数类定义在 `src/pybamm/parameters/geometric_parameters.py` 中，它们的作用是**定义符号化的几何参数**，这些参数随后会被 `ParameterValues` 对象赋予具体数值。

*   **`GeometricParameters`:** 包含通用的几何参数。
*   **`DomainGeometricParameters`:** 定义与宏观域相关的几何参数，例如：
    *   `L_n`: 负极厚度
    *   `L_s`: 隔膜厚度
    *   `L_p`: 正极厚度
    *   `L_cc`: 集流体厚度
    *   `L_y`, `L_z`: 电池单元的宽度和高度 (用于2D/3D集流体模型)
*   **`ParticleGeometricParameters`:** 定义与颗粒子域相关的几何参数，例如：
    *   `R_n_typ`: 典型的负极颗粒半径
    *   `R_p_typ`: 典型的正极颗粒半径

这些符号参数在 `ParameterValues` 类 (如 `pybamm.ParameterValues("Chen2020")`) 中被处理并替换为具体的数值。

## 6. 几何、模型定义和离散化之间的交互

这三者紧密协作，将物理概念转化为可计算的数值问题：

1.  **模型定义 (`pybamm.models`):**
    *   模型定义了变量和方程，并指定了它们作用的 `domain` 和 `auxiliary_domains`。
    *   模型本身不包含具体的坐标值或网格信息。

2.  **参数加载与处理 (`pybamm.ParameterValues`):**
    *   加载参数集，为符号化的几何参数（如 `L_n`, `R_p`）赋予具体数值。
    *   处理后的参数（包含数值化的几何尺寸）会被模型使用。

3.  **几何构建 (`pybamm.Geometry`):**
    *   `pybamm.Geometry` 对象被创建，通常使用如 `pybamm.battery_geometry(model.options, parameter_values)` 这样的辅助函数。
    *   此对象会读取模型选项和已处理的参数值。
    *   `Geometry` 对象为模型中涉及的每个域建立具体的空间坐标变量及其数值范围（例如，`x_n` 的范围是 `0` 到 `L_n` 的具体值）。

4.  **离散化 (`pybamm.Discretisation`):**
    *   `Discretisation` 对象接收模型、`Geometry` 对象和所选的空间离散化方法 (`pybamm.spatial_methods`)。
    *   **网格生成 (`pybamm.Mesh`):** 首先，根据 `Geometry` 为每个域创建相应的子网格 (`SubMesh`)，组合成完整的 `Mesh`。网格包含了离散点（节点）的坐标。
    *   **算子离散化:** 遍历模型中的所有方程和变量。空间微分算子（如 `pybamm.grad`, `pybamm.div`）被替换为基于网格的离散形式（例如，有限体积法中的差分矩阵）。
    *   **变量映射:** 变量被映射到网格上的节点或单元中心。
    *   最终，整个模型被转换为一个大的（通常是稀疏的）微分代数方程组 (DAEs) 或常微分方程组 (ODEs)，可以被数值求解器 (`pybamm.solvers`) 求解。

通过这个流程，PyBaMM 实现了从抽象的物理和数学描述到具体的数值计算的转换，而几何模块在其中扮演了定义“在哪里算”和“坐标是什么”的关键角色。

**返回主目录:** [PyBaMM 项目剖析](./pybamm_main.md)
**上一节:** [参数 (Parameters)](./pybamm_parameters.md)
---
**下一步:** [空间方法与离散化 (Spatial Methods & Discretisations)](./pybamm_discretisation.md)
