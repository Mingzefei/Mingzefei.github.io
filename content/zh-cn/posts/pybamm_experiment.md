# PyBaMM 核心功能：实验 (Experiment)

**返回主目录:** [PyBaMM 项目剖析](./pybamm_main.md)
**上一节:** [仿真 (Simulation)](./pybamm_simulation.md)

---

PyBaMM 中的 `Experiment` 类 (位于 `src/pybamm/experiment/experiment.py`) 允许用户定义一系列操作步骤来模拟电池在特定条件下的行为，例如不同的充放电策略、恒压阶段、休息阶段，或者更复杂的驾驶循环和功率/电流曲线。

## 1. `Experiment` 类的目的

`Experiment` 类的主要目的是：

*   **定义复杂操作序列**: 用户可以通过简单的字符串表示法或直接使用字典列表来定义多步骤的实验。
*   **模拟真实世界场景**: 能够模拟电池的实际使用情况，如GITT（Galvanostatic Intermittent Titration Technique）、HPPC（Hybrid Pulse Power Characterization）、各种驾驶循环（如 US06、WLTP）等。
*   **与 `Simulation` 类集成**: `Experiment` 对象直接传递给 `Simulation` 类，由求解器按照定义的步骤执行。
*   **灵活性**: 支持基于时间、电压、电流、C倍率、SOC（State of Charge）等多种条件的终止和操作。
*   **周期性操作**: 可以定义重复的充放电循环。

## 2. 定义实验步骤

实验由一个或多个操作步骤组成。每个步骤通常定义了电池应如何操作（例如，恒流放电、恒压充电）以及该操作应持续多长时间或在什么条件下终止。

### 2.1. 字符串表示法

最简单直观的方式是使用字符串列表来定义实验。PyBaMM 会解析这些字符串来创建相应的操作指令。

**基本语法**: `"Operation at X unit for Y time_unit or until Z condition"`

*   **Operation**: `Discharge`, `Charge`, `Rest`, `Hold` (通常指恒压)。
*   **X unit**: 操作的幅度和单位。
    *   电流: `A` (安培), `mA` (毫安), `C-rate` (C倍率)。例如 `1 A`, `C/10`, `0.5C`。
    *   功率: `W` (瓦特), `mW` (毫瓦)。例如 `10 W`。
    *   电压 (用于 `Hold`): `V` (伏特), `mV` (毫伏)。例如 `4.2 V`。
*   **Y time_unit**: 操作的持续时间。
    *   `seconds` (或 `s`), `minutes` (或 `min`), `hours` (或 `hr`)。
*   **Z condition** (可选的终止条件):
    *   电压: `V` (伏特)。例如 `until 3.0 V`。
    *   电流 (用于恒压阶段): `A`, `mA`, `C-rate`。例如 `until C/50`。
    *   SOC: `%`。例如 `until 80% SOC`。
    *   温度: `degC` (摄氏度)。例如 `until 45 degC`。

**示例**:

```python
import pybamm

experiment_str = pybamm.Experiment(
    [
        "Discharge at C/10 for 10 hours or until 3.3 V",  # 恒流放电
        "Rest for 1 hour",                               # 静置
        "Charge at 1 A until 4.1 V",                     # 恒流充电
        "Hold at 4.1 V until C/50",                      # 恒压充电，直到电流小于C/50
        "Discharge at 1C until 2.5 V",
        ("Hold at 2.5V for 1 hour",                     # 也可以用元组
         "Charge at C/2 until 4.2V",
         "Hold at 4.2V until C/100"), # 元组可用于组织相关步骤序列，实际的重复周期定义见 2.3 节的 '(...)*N' 语法
    ]
)
```

### 2.2. 字典表示法

或者，实验也可以通过一个字典列表来定义，每个字典代表一个操作步骤。这种方式提供了更精细的控制，但相对繁琐一些。

```python
experiment_dict = pybamm.Experiment(
    [
        {
            "type": "discharge",
            "value": 0.1, "unit": "C-rate",
            "duration": 10, "duration_unit": "hours",
            "termination": {"type": "voltage", "value": 3.3, "unit": "V"}
        },
        {
            "type": "rest",
            "duration": 1, "duration_unit": "hours"
        },
        # ... 其他步骤
    ]
)
```
PyBaMM 内部会将字符串表示法转换为这种字典结构进行处理。

### 2.3. 周期和子实验

可以通过将步骤列表嵌套在元组中并后跟一个数字来定义重复周期。

```python
experiment_cycling = pybamm.Experiment(
    [
        "Charge at 1C until 4.2V",
        "Hold at 4.2V until C/50",
        (
            "Discharge at 1C until 3.0V",
            "Charge at 1C until 4.2V",
            "Hold at 4.2V until C/50",
        ) * 10, # 将这个放电-充电-恒压序列重复10次
        "Rest for 30 minutes"
    ]
)
```

### 2.4. 特殊指令

*   **`period`**: 可以为每个操作步骤或整个实验指定 `period` 参数，这定义了求解器保存数据点的时间间隔。例如：`"Discharge at 1 A for 1 hour period 60 s"` (每60秒保存一次数据)。
*   **`temperature`**: 可以为每个步骤或整个实验设置环境温度。例如：`"Discharge at C/5 for 2 hours temperature 25 degC"`。
*   **`events` (记录事件)**: 用户可以定义在实验过程中需要监测和记录的特定条件。这些事件的发生不会终止当前的实验步骤（步骤终止由时长或 `until` 条件控制），但其发生的时间和状态会被记录在 `Solution` 对象中，便于后续分析。
    *   **全局记录事件**: 在 `Experiment` 初始化时，可以通过 `events` 参数（一个字符串列表）指定对整个实验生效的记录事件。列表中的每个字符串应对应模型中的一个变量或一个表达式，当该表达式变为非零时，事件被记录。例如: `events=["Minimum negative particle surface concentration [mol.m-3] < 0.001", "Cell temperature [degC] > 45"]`。
    *   **步骤特定记录事件 (通过字典定义)**: 在使用字典列表定义实验步骤时，每个步骤的字典可以包含一个 `\"events\"` 键。其值是一个字符串列表，定义了该步骤中需要额外监测和记录的事件。列表中的每个字符串应对应模型中的一个变量或一个表达式，当该表达式变为非零时，事件被记录。例如: `{\"type\": \"discharge\", ..., \"events\": [\"State of charge [%] < 20.5\", \"Cell temperature [degC] > 44.5\"]}`。
    *   **注意**: 目前，在标准的实验步骤字符串表示法中直接嵌入步骤特定的记录事件定义并不常见或支持。推荐使用字典格式定义实验步骤，或使用全局记录事件，以实现对事件记录的精细控制。
*   **`drive_cycles`**: 可以加载外部文件（如CSV）作为驱动循环，其中包含时间序列的电流、功率或电压数据。例如：`"Drive cycle from file: drive_cycle.csv"`。文件应包含两列：时间 (s) 和对应的值 (A, W, 或 V)。

## 3. `Experiment` 类的内部工作原理

1.  **解析**: 当创建 `Experiment` 对象时，输入的字符串列表或字典列表会被解析成一个标准的内部操作指令列表。每个指令都是一个字典，包含了操作类型、值、单位、持续时间、终止条件等详细信息。
2.  **转换**: 这些操作指令会进一步转换为求解器可以理解的格式。例如，“C-rate”会根据 `Simulation` 对象中提供的 `C_rate` 和标称容量转换为具体的电流值。
3.  **与求解器交互**: 在 `sim.solve()` 过程中，`Simulation` 对象会按顺序将实验的每个步骤传递给求解器。
    *   求解器根据当前步骤的定义（如恒流、恒压）来设置模型的边界条件或源项。
    *   求解器会监控该步骤的终止条件（例如，达到某个电压、持续时间结束、电流降至某个值）。
    *   一旦一个步骤的终止条件满足，求解器会停止，保存该步骤的解，然后 `Simulation` 对象会准备并启动实验中的下一个步骤，直到所有步骤完成或某个全局终止条件满足。

## 4. 使用 `Experiment` 的好处

*   **标准化测试**: 轻松实现标准的电池测试程序。
*   **复杂场景模拟**: 能够模拟复杂的实际应用场景，如电动汽车的驾驶循环。
*   **参数敏感性分析**: 结合参数集，可以研究不同操作条件下电池性能的变化。
*   **模型验证**: 通过将仿真结果与在相同实验条件下获得的实验数据进行比较来验证模型。

## 5. 示例：GITT 实验

GITT 是一种常用的电化学技术，用于确定电极材料的化学扩散系数。它包括一系列短的恒流脉冲，然后是长时间的静置，以使浓度在电极内达到平衡。

```python
# GITT 示例: 10个 C/20 的放电脉冲，每个持续6分钟，然后休息30分钟
# 整个过程在电压低于3.0V时终止
gitt_experiment = pybamm.Experiment(
    [
        ("Discharge at C/20 for 6 minutes", "Rest for 30 minutes") * 10
    ],
    termination="3.0V"
)

# model = pybamm.lithium_ion.DFN()
# param = pybamm.ParameterValues("Chen2020")
# sim = pybamm.Simulation(model, experiment=gitt_experiment, parameter_values=param, solver=pybamm.CasadiSolver())
# sol = sim.solve()
# sol.plot([
#     "Current [A]",
#     "Terminal voltage [V]",
#     "Electrolyte concentration [mol.m-3]",
#     "Negative particle surface concentration [mol.m-3]",
#     "Positive particle surface concentration [mol.m-3]",
# ])
```

## 6. 总结

PyBaMM 的 `Experiment` 类为定义和执行复杂的电池操作序列提供了一个强大而灵活的工具。通过其直观的字符串表示法和对各种操作条件的支持，用户可以轻松地模拟从标准测试协议到定制驾驶循环的各种场景，从而深入了解电池在不同条件下的行为和性能。

---

**下一步:** [绘图与后处理 (Plotting & Solution Processing)](./pybamm_plotting_and_processing.md)
