# CLAUDE.md - AI Coding Assistant Configuration

> Inspired by VMark (xiaolai/vmark) - A modern AI-native Markdown editor

---

## Project Overview

[项目名称] - [简短描述]

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | [语言] |
| Framework | [框架] |
| Package Manager | [pnpm/npm/yarn] |
| Build Tool | [构建工具] |
| Runtime | [Node.js/Python/etc] |

---

## Development Rules

### Code Quality

- **File size limit**: ~300 lines per file (split larger files)
- **Naming conventions**: [说明命名规范]
- **Code style**: [Prettier/ESLint配置]
- **Type safety**: [TypeScript strict mode/etc]

### Git Workflow

```
Branch: feature/xxx | fix/xxx | refactor/xxx
Commit: <type>(<scope>): <description>

Types:
- feat: 新功能
- fix: Bug修复
- refactor: 重构
- docs: 文档更新
- test: 测试
- chore: 维护
```

### Security Principles

1. 禁止执行未审查的外部代码
2. 涉及文件删除需二次确认
3. 敏感操作（网络请求、API调用）需说明用途
4. 不在代码中硬编码密钥

---

## Guardians (守护机制)

### TDD Guardian

**核心原则**: 测试先行

1. **新功能开发**:
   ```
   需求 → 写测试 → 写代码 → 测试通过 → 重构
   ```

2. **Bug修复**:
   ```
   复现 → 写测试 → 修复 → 测试通过
   ```

3. **覆盖率要求**:
   - 核心逻辑覆盖率 > 80%
   - 新增代码必须有测试

4. **禁止**:
   - 先写代码后补测试
   - 绕过测试提交代码
   - 删除或禁用现有测试

### Docs Guardian

**核心原则**: 文档与代码同步

1. **触发时机**:
   - 修改 API 接口
   - 添加新功能
   - 删除废弃功能
   - 修改配置项

2. **同步要求**:
   - API 变更 → 更新 API 文档
   - 配置变更 → 更新 README/配置说明
   - 新功能 → 添加使用示例

3. **禁止**:
   - 文档与代码不一致
   - 过期的示例代码
   - 未更新的 changelog

### Lint Guardian

1. 提交前必须通过所有 lint 检查
2. 自动修复可修复的问题
3. 不可自动修复的问题需手动处理

---

## Commands (自定义命令)

### `/init`
初始化项目配置，创建 CLAUDE.md

### `/review`
代码质量审查
- 检查命名规范
- 识别潜在问题
- 提供优化建议

### `/test`
运行测试套件
- 执行所有测试
- 显示覆盖率报告
- 失败时显示详细错误

### `/lint`
代码检查
- 运行 lint 工具
- 自动修复可修复问题
- 报告剩余问题

### `/build`
生产构建
- 执行完整构建
- 验证产物完整性
- 检查资源文件

### `/tdd`
TDD 模式
- 创建测试文件
- 运行测试监视
- 切换测试/代码视图

### `/docs`
文档检查
- 验证文档与代码一致性
- 检查过时内容
- 生成更新建议

---

## Project Structure

```
.
├── src/              # 源代码
│   ├── components/   # UI 组件
│   ├── hooks/        # 自定义 Hooks
│   ├── utils/        # 工具函数
│   └── types/        # 类型定义
├── tests/            # 测试文件
│   ├── unit/         # 单元测试
│   ├── integration/   # 集成测试
│   └── e2e/          # 端到端测试
├── docs/             # 文档
├── scripts/          # 构建脚本
└── configs/          # 配置文件
```

---

## UI Development Rules

### Design System

1. **设计 Token**: 所有颜色/间距/字体使用 CSS 变量
2. **组件模式**: 使用组合而非继承
3. **状态管理**: 使用 Zustand/Pinia，组件内禁止直接修改 store
4. **响应式**: 移动优先设计

### Color Scheme

```css
/* Light Mode */
--bg-primary: #ffffff;
--bg-secondary: #f5f5f5;
--text-primary: #1a1a1a;
--text-secondary: #666666;
--accent: #007aff;

/* Dark Mode */
--bg-primary: #1a1a1a;
--bg-secondary: #2d2d2d;
--text-primary: #ffffff;
--text-secondary: #999999;
--accent: #0a84ff;
```

### Focus Indicators

- 所有可交互元素必须有 focus 样式
- 使用 `outline` 而非 `box-shadow`
- 键盘导航时显示焦点指示

---

## Success Criteria

项目成功的标准：

| 检查项 | 要求 |
|--------|------|
| 测试通过 | 100% |
| Lint 检查 | 无 warning |
| 文档同步 | 与代码一致 |
| 类型安全 | 无 any |
| 代码覆盖 | > 80% |

---

## Tips for Claude Code

### 常用快捷键

- `Ctrl+G` - 跳转到文件
- `Ctrl+R` - 搜索命令历史
- `Ctrl+L` - 清除对话
- `Ctrl+Shift+P` - 打开命令面板

### 有用参数

- `--dangerously-skip-permissions` - 跳过权限提示（谨慎使用）
- `/model` - 切换 AI 模型
- `/help` - 查看所有命令

---

## Custom Instructions

[在这里添加项目特定的自定义指令]

---

## Environment Setup

### Required

- Node.js 20+
- pnpm 10+
- [其他必需工具]

### Optional

- Rust (用于 Tauri)
- Docker (用于容器化)

### Environment Variables

```
# .env.example
NODE_ENV=development
API_URL=http://localhost:3000
```