/**
 * weekly-update 勾选归档交互
 * 在「状态」列添加 checkbox，勾选后保存到 localStorage
 * 配合「对我说」的归档指令工作流
 */
document.addEventListener('DOMContentLoaded', function() {
  // 找到待归档表格
  const table = document.querySelector('table');
  if (!table) return;

  const STORAGE_KEY = 'weekly_archive_checks';

  // 从 localStorage 恢复状态
  let savedState = {};
  try {
    savedState = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
  } catch(e) {}

  // 遍历表格行（跳过表头）
  const rows = table.querySelectorAll('tbody tr, tr:not(:first-child)');
  rows.forEach(function(row) {
    const cells = row.querySelectorAll('td');
    if (cells.length < 5) return;

    // 状态列（第5列，index=4）
    const statusCell = cells[4];
    const paperKey = cells[0]?.textContent?.trim() || '';

    // 创建 checkbox
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.style.transform = 'scale(1.3)';
    checkbox.style.cursor = 'pointer';
    checkbox.title = '勾选后标记为已归档（状态保存在本地浏览器）';

    // 恢复勾选状态
    if (savedState[paperKey]) {
      checkbox.checked = true;
      row.style.opacity = '0.5';
      row.style.textDecoration = 'line-through';
    }

    // 勾选事件
    checkbox.addEventListener('change', function() {
      if (this.checked) {
        savedState[paperKey] = true;
        row.style.opacity = '0.5';
        row.style.textDecoration = 'line-through';
        statusCell.textContent = '✅ 已归档';
      } else {
        delete savedState[paperKey];
        row.style.opacity = '1';
        row.style.textDecoration = 'none';
        statusCell.textContent = '待归档';
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(savedState));
    });

    // 清空状态列原内容，放入 checkbox
    statusCell.innerHTML = '';
    statusCell.style.textAlign = 'center';
    statusCell.appendChild(checkbox);

    // 如果已勾选，显示文字
    if (checkbox.checked) {
      const label = document.createElement('span');
      label.textContent = ' ✅';
      label.style.fontSize = '0.85em';
      statusCell.appendChild(label);
    }
  });

  // 添加「清空勾选」按钮
  const pageContent = document.querySelector('.md-content');
  if (pageContent) {
    const btn = document.createElement('div');
    btn.style.cssText = 'margin-top: 1em; text-align: right;';
    btn.innerHTML = '<button id="clear-archives" style="padding: 6px 16px; cursor: pointer; border: 1px solid var(--md-default-fg-color--light); border-radius: 4px; background: transparent; color: var(--md-default-fg-color); font-size: 0.85rem;">🗑️ 清空所有勾选</button>';
    pageContent.appendChild(btn);

    document.getElementById('clear-archives')?.addEventListener('click', function() {
      if (confirm('确定清空所有勾选状态？不会影响已归档的论文文件。')) {
        localStorage.removeItem(STORAGE_KEY);
        location.reload();
      }
    });
  }
});
