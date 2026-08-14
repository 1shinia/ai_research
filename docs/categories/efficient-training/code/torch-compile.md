# torch.compile

## 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | torch.compile |
| **语言** | Python / C++ |
| **用途** | PyTorch JIT 编译优化 |
| **GitHub** | [pytorch/pytorch](https://github.com/pytorch/pytorch) |
| **许可证** | BSD-3 |

## 简介

PyTorch 2.x 引入的 JIT 编译器 `torch.compile`，通过将模型转换为计算图并进行内核融合优化，在 GPU 上实现显著加速。支持 eager 模式的无缝切换，一行代码即可获得 1.5-3x 的推理 / 训练加速。

## 核心功能

- **TorchDynamo**: Python 字节码级图捕获
- **TorchInductor**: 生成 Triton / CUDA 内核
- **后端选择**: Inductor / NVFuser / ONNX Runtime
- **模式**: default / reduce-overhead / max-autotune
- 支持训练和推理两种场景

## 快速开始

```python
import torch

model = MyModel().cuda()
opt_model = torch.compile(model, mode="reduce-overhead")

# 训练循环（接口完全不变）
output = opt_model(input_data)
loss = output.sum()
loss.backward()
```

## 使用场景

- PyTorch 模型推理加速（1.5-3x）
- PyTorch 训练加速（~1.5x）
- 生产部署中的性能优化

---

*此页面的项目信息由 AI Research Tracker 自动维护。*
