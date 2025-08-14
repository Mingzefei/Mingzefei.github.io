# PyBaMM 核心功能：绘图与后处理 (Plotting and Processing)

**返回主目录:** [PyBaMM 项目剖析](./pybamm_main.md)
**上一节:** [实验 (Experiment)](./pybamm_experiment.md)

---

在 PyBaMM 中，仿真结果的分析和可视化是理解模型行为和电池性能的关键环节。PyBaMM 提供了内置的绘图功能以及与其他流行数据分析和可视化库（如 Matplotlib, NumPy, Pandas）的良好兼容性，方便用户进行深入的后处理。

## 1. `Solution` 对象：结果的容器

当 `Simulation.solve()` 或 `Simulation.step()` 方法成功执行后，会返回一个 `pybamm.Solution` 对象 (或在 `sim.solution` 中累积)。这个对象是所有仿真数据的中心，包含了：

*   **时间点 (`solution.t`)**: 求解器实际采用的时间步长数组。个人认为，理解这些时间点并非总是等间隔的非常重要，尤其是在使用自适应步长的求解器时。
*   **状态向量 (`solution.y`)**: 在每个时间点上，模型中所有状态变量的值。这是一个二维数组，行对应状态变量，列对应时间点。个人推测，这个原始状态向量对于普通用户可能不那么直观，通常会通过 `solution.processed_variables` 来访问更有意义的物理量。
*   **模型变量 (`solution.model.variables`)**: 一个字典，包含了模型中定义的所有变量的符号表示。
*   **已处理的变量 (`solution.processed_variables`)**: 一个字典，存储了 `pybamm.ProcessedVariable` 对象。这些对象是在求解后根据模型变量和状态向量计算得到的，可以直接用于绘图和分析。
*   **终止信息**: `solution.termination` (终止原因字符串), `solution.t_event` (事件发生的时间), `solution.y_event` (事件发生时的状态向量)。
*   **输入参数 (`solution.inputs`)**: 仿真过程中使用的输入参数。
*   **子解 (对于实验)**: 如果仿真包含多个实验步骤，`solution.cycles` 或 `solution.steps` 属性可以用来访问每个独立步骤的解。

## 2. 访问和处理变量

### 2.1. 通过键访问变量

最直接的方式是通过变量名字符串从 `Solution` 对象中获取已处理的变量：

```python
import pybamm

# 假设已经运行了仿真并得到了 solution 对象
# solution = sim.solve()

# 获取端电压
terminal_voltage = solution["Terminal voltage [V]"]

# 获取负极颗粒表面浓度
# 注意：对于空间分布的变量，其 .data 属性通常是二维或三维的 (空间维度 x 时间)
neg_particle_surf_conc = solution["Negative particle surface concentration [mol.m-3]"]

# 查看变量的数据和对应的时间点
# print(terminal_voltage.data) # 一维数组，对应每个 solution.t
# print(neg_particle_surf_conc.t) # 通常与 solution.t 相同
# print(neg_particle_surf_conc.data) # 二维数组 (位置 x 时间)
```

`solution[var_name]` 返回的是一个 `pybamm.ProcessedVariable` 对象。其主要属性有：
*   `.data`: 变量在各个时间点和空间点（如果适用）的数值。
*   `.t`: 对应的时间点数组。
*   `.x`, `.r_n`, `.r_p`, `.z` 等: 对应的空间坐标点数组（如果变量在这些域上定义）。
*   `.entries`: 对于向量或张量型变量，这是其各个分量的 `ProcessedVariable` 对象列表。

### 2.2. 对变量进行操作

`ProcessedVariable` 对象重载了许多算术运算符，允许直接对它们进行计算，结果通常也是 `ProcessedVariable` 对象或 NumPy 数组。

```python
# 示例：计算过电位 (假设 Eta_r 和 Eta_e 是已处理变量)
# eta_r = solution["Reaction overpotential [V]"]
# eta_e = solution["Electrolyte overpotential [V]"]
# total_overpotential = eta_r + eta_e # 逐点相加

# 也可以直接对 .data 操作 (返回 NumPy 数组)
# voltage_times_two = terminal_voltage.data * 2
```

### 2.3. 插值

`Solution` 对象本身以及 `ProcessedVariable` 对象都可以像函数一样被调用，以在新的时间点（或空间点）上进行插值。

```python
# 在新的时间点 t_new 上插值整个解 (所有变量)
# t_new = np.linspace(0, solution.t[-1]/2, 100)
# interpolated_solution_at_t_new = solution(t_new)
# 个人理解：调用 solution(t_new) 会对所有已处理的变量在 t_new 上进行插值，并返回一个新的 Solution 对象，其 .t 和 .y 以及 processed_variables 都会更新为插值后的结果。

# 对单个变量进行插值
# new_voltages = terminal_voltage(t_new) # 返回一个包含插值电压的 NumPy 数组
# 个人理解：调用 processed_variable(t_new) 通常返回一个 NumPy 数组，包含该变量在 t_new 上的插值数据。

# 对于空间变量，可以指定空间坐标进行插值
# x_interest = np.array([0.1, 0.5, 0.9]) # 假设 x 是归一化长度
# conc_at_x_interest_and_t_new = neg_particle_surf_conc(t_new, x=x_interest)
# 结果维度将是 (len(x_interest), len(t_new))
# 个人推测：对于空间变量的插值，如果原始数据是离散的网格点，这里会使用适当的插值方法（如线性或样条插值）来估计指定空间点的值。
```

## 3. 内置绘图功能 (`solution.plot()`)

PyBaMM 的 `Solution` 对象带有一个便捷的 `plot` 方法，用于快速可视化结果。它底层使用 Matplotlib。

```python
# 绘制一组预定义的默认变量
# solution.plot()

# 绘制指定的变量列表
# solution.plot(output_variables=[
#     "Current [A]",
#     "Terminal voltage [V]",
#     "Negative electrode potential [V]",
#     "Positive electrode potential [V]",
#     "Electrolyte concentration [mol.m-3]"
# ])

# 控制绘图选项
# fig = solution.plot(
#     output_variables=["Terminal voltage [V]", "Current [A]"],
#     time_unit="hours", # 时间单位 (seconds, minutes, hours)
#     spatial_unit="um", # 空间单位 (m, mm, um)
#     show_legend=True,
#     show_plot=True, # 是否立即显示图像
#     testing=False # 设为 True 则不显示，用于测试
# )
# fig[0].savefig("voltage_current_plot.png") # fig 是一个包含 matplotlib.Figure 对象的列表
```

`solution.plot()` 会自动处理不同维度变量的绘图：
*   **0D 变量** (如端电压, 电流): 绘制为时间序列图。
*   **1D 变量** (如电解质浓度沿 x 轴分布): 通常会生成一个二维图（x轴 vs 时间，颜色表示值）或在特定时间点/空间点的切片图。
*   **2D 变量** (如颗粒内浓度 r vs x): 可能生成动画或特定时间/空间切片的图像。

## 4. `QuickPlot` 类：更灵活的绘图

`pybamm.QuickPlot` 类 (位于 `pybamm/plot/quick_plot.py`) 提供了比 `solution.plot()` 更细致的绘图控制。它允许用户指定要绘制的 `Simulation` 对象（或 `Solution` 列表）、变量、绘图布局、时间单位等。

```python
import pybamm
import numpy as np # 确保导入 numpy 用于示例中的 np.linspace

# 假设 sim1, sim2 是两个不同的 Simulation 对象 (或已求解的 Solution)
# model = pybamm.lithium_ion.DFN()
# param = pybamm.ParameterValues("Marquis2019")
# sim1 = pybamm.Simulation(model, parameter_values=param)
# sim2 = pybamm.Simulation(model, parameter_values=param) # 示例中用同一个模型和参数，实际可不同
# sol1 = sim1.solve([0, 3600])
# sol2 = sim2.solve([0, 3600]) # 实际应用中，对比的解通常来自不同模型或参数

# output_vars = ["Terminal voltage [V]", "Current [A]"]
# plot = pybamm.QuickPlot([sol1, sol2], output_variables=output_vars, labels=["DFN Solution 1", "DFN Solution 2"])
# plot.plot(0) # 绘制时间 t=0 的图像 (对于时间序列通常是整个序列)
# plot.dynamic_plot() # 创建一个交互式动态图 (需要 ipywidgets)
# # plot.fig.savefig("comparison_plot.png") # QuickPlot 对象本身没有 fig 属性，需要从 plot.plots 字典中获取 fig
# if plot.plots:  # 检查是否有图像生成
#     # QuickPlot 可能为每个输出变量生成一个子图，或者将它们组合。
#     # 这里假设我们保存第一个生成的图像的 Figure 对象。
#     # 具体的 Figure 对象需要根据 plot.plots 的结构来获取。
#     # 例如，如果 output_vars 中的每个变量都在独立的 Figure 中：
#     # first_var_key = list(plot.plots.keys())[0]
#     # fig_to_save = plot.plots[first_var_key]["fig"]
#     # fig_to_save.savefig("comparison_plot.png")
#     # 或者，如果所有变量共享一个 Figure，可能需要不同的访问方式。
#     # 对于 plot.plot(0) 生成的静态图，通常会有一个主 Figure 对象。
#     # 更稳妥的方式是查阅 QuickPlot 的具体实现或文档来确定如何访问 Figure 对象。
#     # 暂时注释掉保存部分，因为访问 fig 的方式不确定
```

`QuickPlot` 的主要功能：
*   **比较多个解**: 可以将多个 `Solution` 对象绘制在同一张图上进行比较。
*   **动态图 (`dynamic_plot`)**: 创建可以通过滑块交互式地改变时间点的动态图，非常适合观察空间变量随时间的变化。
*   **动画 (`create_gif` 或 `create_animation`)**: 将动态图保存为 GIF 或其他视频格式。
*   **自定义 Matplotlib 轴**: 用户可以提供自己的 Matplotlib `Axes` 对象进行绘图。

## 5. 导出数据

仿真结果可以方便地导出为常见的数据格式，以便在其他软件中进行分析或存档。

### 5.1. 保存 `Solution` 对象

整个 `Solution` 对象（或 `Simulation` 对象）可以被序列化（pickle）：

```python
# solution.save("my_solution.pkl")
# loaded_solution = pybamm.load_solution("my_solution.pkl")

# sim.save("my_simulation.pkl")
# loaded_sim = pybamm.load_simulation("my_simulation.pkl")
```

### 5.2. 保存为 CSV 或 MATLAB .mat 文件

`Solution` 对象提供了 `save_data` 方法：

```python
# 保存所有变量到 CSV (每个变量一个文件，文件名基于变量名)
# solution.save_data("solution_data_all.csv", variables=None, to_format="csv", short_names=None)
# 个人认为：当 variables=None 时，PyBaMM 会尝试保存模型中定义的所有变量，这可能会产生大量文件，适用于需要全面数据备份的场景。

# 保存指定变量到单个 CSV 文件
# solution.save_data(
#     "selected_data.csv",
#     variables=["Time [s]", "Current [A]", "Terminal voltage [V]"],
#     to_format="csv"
# )
# 个人推测：当指定 variables 列表并使用 to_format="csv" 时，如果这些变量具有相同的时间基准，它们可能会被合并到一个CSV文件中，列名为变量名。
# 如果变量具有不同的维度或时间基准，行为可能有所不同，可能仍会生成多个文件或引发错误，具体需查阅文档或测试。

# 保存到 MATLAB .mat 文件
# solution.save_data("solution_data.mat", to_format="matlab")
# 个人理解：保存为 .mat 文件会将 Solution 对象中的数据（可能是所有 processed_variables）打包到一个 MATLAB 可读的文件中，方便在 MATLAB 环境中进行后续分析。
```

导出的数据可以直接加载到 Pandas DataFrame 或 MATLAB 中进行进一步处理。

## 6. 与其他库集成

由于 PyBaMM 的变量数据通常以 NumPy 数组的形式存在，因此很容易与 NumPy, SciPy, Pandas, Matplotlib, Seaborn 等库集成，进行高级数据分析、统计和定制化绘图。

```python
# import pandas as pd
# import matplotlib.pyplot as plt

# # 获取数据到 Pandas DataFrame
# time_s = solution["Time [s]"].data
# voltage_V = solution["Terminal voltage [V]"].data
# current_A = solution["Current [A]"].data

# df = pd.DataFrame({
#     "Time [s]": time_s,
#     "Voltage [V]": voltage_V,
#     "Current [A]": current_A
# })

# print(df.describe())

# # 使用 Matplotlib 自定义绘图
# plt.figure()
# plt.plot(df["Time [s]"], df["Voltage [V]"], label="Voltage")
# plt.xlabel("Time [s]")
# plt.ylabel("Voltage [V]")
# plt.legend()
# plt.show()
```

## 7. 总结

PyBaMM 提供了从快速概览到深度分析的全面后处理和可视化工具。`Solution` 对象是所有结果数据的核心，通过其内置方法和与 Python 生态系统中其他强大库的兼容性，用户可以有效地提取、处理、可视化和导出仿真数据，从而深入理解电池模型的行为并验证其预测。

---

**返回主目录:** [PyBaMM 项目剖析](./pybamm_main.md)
