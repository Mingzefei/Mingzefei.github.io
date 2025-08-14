# PyBaMM 核心子系统：模型 (Models) - 构建电池世界的蓝图

**返回主目录:** [PyBaMM 项目剖析](./pybamm_main.md)
**上一节:** [表达式树 (Expression Tree)](./pybamm_expression_tree.md)

---

在探讨了表达式树奠定的符号基础之后，我们现在转向 PyBaMM 如何利用这个基础来构建**模型 (Models)**。`models` 模块（主要位于 `src/pybamm/models/`）是电池物理和化学栩栩如生的地方。它关乎将电池如何工作的概念性理解转化为 PyBaMM 可以求解的一组具体的数学方程。

## 1. 理念：模块化与可重用性

电池是复杂的系统。一个完整的物理模型可能涉及电化学、热力学、力学和降解现象。整体处理这个问题对于开发、测试和定制来说将是一场噩梦。

PyBaMM 的作者为其模型采用了一种**模块化设计理念**。其核心思想是：
*   **分解：** 一个完整的电池模型（如 Doyle-Fuller-Newman, DFN, 或单粒子模型, SPM）被分解成更小、更易于管理的**子模型 (submodels)**。每个子模型描述一个特定的物理过程或组件（例如，电解质扩散、电极动力学、热效应、颗粒力学）。
*   **标准化接口：** 子模型被设计为具有相对标准的输入和输出，允许它们以即插即用方式组合。
*   **可重用性：** 一个定义良好的子模型（例如，用于电解质中菲克扩散的子模型）可以在不同的主要电池模型中重用。
*   **定制化：** 用户可以轻松地用自定义子模型替换默认子模型（例如，实现新的降解机制），而无需更改主模型结构的其余部分。

这种方法显著增强了 PyBaMM 的灵活性和可扩展性。

## 2. `BaseBatteryModel`：所有电池模型的蓝图

模型系统的核心是 `pybamm.BaseBatteryModel` 类 (位于 `src/pybamm/models/base_battery_model.py`)。这个抽象基类充当 PyBaMM 中所有特定电池模型的蓝图。它本身不定义任何特定的物理特性，但它确立了构建电池模型及其控制方程组装的**结构和过程**。

**为什么需要 `BaseBatteryModel`？**
*   **一致性：** 它确保所有电池模型，无论其具体物理特性如何（例如，铅酸电池与锂离子电池，DFN 与 SPM），在定义变量、方程、边界条件和初始条件时都遵循一致的结构。
*   **编排：** 它通过以预定义的顺序调用其组成子模型的方法来编排完整模型的构建。
*   **集中存储：** 它充当定义模型的所有符号方程（`rhs`、`algebraic`、`initial_conditions`、`boundary_conditions`、`variables`）的中央存储库。

**`BaseBatteryModel` 的主要职责和工作流程：**

1.  **初始化 (`__init__`)**：接受一个 `name` 和一个 `options` 字典。`options` 字典至关重要，因为它允许用户选择不同的子模型或指定要包含/排除的某些物理效应（例如，`options={"thermal": "lumped"}` vs `options={"thermal": "x-full"}`）。
2.  **子模型实例化**：根据提供的 `options`，`BaseBatteryModel`（或其具体子类，如 `lithium_ion.BaseModel`）实例化所选的子模型。例如，如果 `options["particle"]` 是 "Fickian diffusion"，它将创建一个菲克扩散颗粒子模型的实例。
3.  **构建模型 (`_build_model` 及相关方法)：** 这是奇迹发生的地方。`BaseBatteryModel` 系统地调用其子模型的方法以获取相关的方程和变量：
    *   `get_fundamental_variables()`：每个子模型定义其基本变量（例如，浓度、电势）。
    *   `get_coupled_variables()`：子模型定义可能依赖于其他子模型变量的变量。
    *   `set_rhs()`：子模型为其 ODE 定义右侧项（时间导数）。
    *   `set_algebraic()`：子模型定义其代数约束。
    *   `set_boundary_conditions()`：子模型为 PDE 定义边界条件。
    *   `set_initial_conditions()`：子模型定义其变量的初始状态。
    *   `set_events()`：子模型可以定义可能终止仿真的事件（例如，电压截止）。
4.  **存储方程：** 所有这些符号方程（它们是来自表达式树的 PyBaMM `Symbol` 对象）都被收集并存储在 `BaseBatteryModel` 实例内的字典中（例如，`self.rhs`、`self.algebraic`、`self.variables`）。

从本质上讲，`BaseBatteryModel` 扮演着指挥家的角色，引导每个子模型（音乐家）为整个交响乐（完整的模型方程组）贡献自己的部分。

## 3. 具体电池模型：DFN、SPM 及其他

PyBaMM 附带了几个预构建的电池模型，最著名的是锂离子化学模型：

*   **`pybamm.lithium_ion.DFN` (Doyle-Fuller-Newman 模型)：** (例如，在 `src/pybamm/models/lithium_ion/dfn.py` 中)
    *   一个综合模型，通常包括电解质中的扩散、固体颗粒中的扩散（通常假设球形对称）以及电化学反应的 Butler-Volmer 动力学。
    *   它继承自 `pybamm.lithium_ion.BaseModel`，而后者又继承自 `BaseBatteryModel`。
    *   其 `__init__` 方法调用 `super().__init__(options, name)`，然后设置构成 DFN 的特定子模型组合。

*   **`pybamm.lithium_ion.SPM` (单粒子模型)：** (例如，在 `src/pybamm/models/lithium_ion/spm.py` 中)
    *   一个简化模型，假设整个电极的行为类似于单个代表性粒子，在许多情况下忽略了电解质动力学。
    *   它也继承自 `pybamm.lithium_ion.BaseModel`。

**`options` 字典：定制的关键**

当你创建一个模型实例时，例如 `model = pybamm.lithium_ion.DFN(options={"thermal": "x-full"})`，`options` 字典会通过模型层次结构向下传递。像 `DFN` 这样的具体模型及其子模型使用这些选项来决定：
*   要包括哪些特定的物理效应（例如，热效应、颗粒应力、SEI 生长）。
*   对特定现象使用哪种数学公式（例如，颗粒中的“菲克扩散”与“均匀”浓度）。

这种 `options` 机制是 PyBaMM 灵活性的基石。它允许用户轻松探索不同建模假设的影响，而无需编写全新的模型类。

## 4. 子模型：构建模块

子模型是定义物理特性的真正主力军。它们通常位于 `src/pybamm/models/submodels/` 之类的目录中。每个子模型都专注于电池行为的特定方面。

**子模型类别示例：**
*   `particle/`：电极颗粒内的固相扩散（例如，`fickian_diffusion.py`、`uniform_profile.py`）。
*   `electrolyte_conductivity/`：电解质中的离子传输（例如，`base_electrolyte_conductivity.py`、`full_conductivity.py`）。
*   `electrode_kinetics/`：用于电荷转移反应的 Butler-Volmer 或 Tafel 动力学（例如，`base_kinetics.py`）。
*   `thermal/`：生热和散热（例如，`lumped.py`、`x_full.py`）。
*   `porosity/`：由于反应或降解引起的孔隙率变化。
*   `interface/`：SEI 层生长、锂析出等。

**典型子模型的结构 (例如 `src/pybamm/models/submodels/particle/fickian_diffusion.py`)：**

*   它继承自一个基础子模型类 (例如 `pybamm.particle.BaseParticle`)。
*   `get_fundamental_variables()`：定义诸如“X-平均负极颗粒浓度 [mol.m-3]”之类的变量。
*   `get_coupled_variables()`：可能根据平均浓度计算表面浓度之类的值。
*   `set_rhs(variables)`：定义颗粒内菲克扩散的 PDE，例如 `d(c_s)/dt = div(D_s * grad(c_s))`。这个方程将使用表达式树中的 `Symbol` 对象构建。
*   `set_boundary_conditions(variables)`：定义颗粒中心（对称性）和表面（与电流相关的通量）的边界条件。
*   `set_initial_conditions(variables)`：设置颗粒中的初始浓度分布。

传递给这些方法的 `variables` 参数是一个字典，其中包含模型其他部分已定义的符号，从而允许子模型相互耦合。

## 5. 定义新模型或修改现有模型

理解这种模块化结构是扩展 PyBaMM 的关键：

*   **创建现有模型的新变体：** 通常只需将不同的 `options` 传递给现有模型类即可。
*   **引入新的物理现象：** 通常需要编写一个新的子模型类。该类将定义其自己的变量和方程。然后，你需要修改现有的主模型类（或创建一个继承自 `BaseBatteryModel` 或更具体的基类如 `lithium_ion.BaseModel` 的新类），以在其 `_build_model` 过程中包含你的新子模型，并可能通过 `options` 字典中的新条目进行控制。
*   **定义一个全新的电池模型类型（例如，针对不同的化学体系）：** 你可能需要创建一个继承自 `BaseBatteryModel` 的新类，定义其特定的子模型组件，并管理它们之间的交互。

## 6. 设计原理 - 总结

PyBaMM 中的模型架构反映了一个清晰的策略：
*   **分而治之：** 将电池物理的复杂性分解为可管理的子模型单元。
*   **促进可重用性：** 设计子模型，使其可以在多种环境中使用。
*   **通过选项实现定制：** 允许用户轻松配置模型，而无需进行深层代码更改。
*   **标准化构建过程：** 使用 `BaseBatteryModel` 确保所有模型都以一致的方式构建并收集其方程。

这种结构不仅使 PyBaMM 开箱即用功能强大，而且使其成为未来电池建模研究和开发的高度适应性框架。

---

**下一步:** [参数 (Parameters)](./pybamm_parameters.md)
