#!/bin/bash
# Скрипт сборки единого отчёта из секций
# Использование: bash docs/practice/build_report.sh
# Результат: docs/practice/report.txt — полный отчёт, готовый к печати

set -e

REPORT_DIR="report_sections"
OUTPUT_FILE="report.txt"

echo "Сборка отчёта из секций..."

# Заголовок
echo "ОТЧЁТ ПО ПРОИЗВОДСТВЕННОЙ ПРАКТИКЕ" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "Собран автоматически из секций. Дата сборки: $(date '+%Y-%m-%d %H:%M')" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Сборка секций в порядке нумерации
for section_file in "$REPORT_DIR"/00_*.txt \
                    "$REPORT_DIR"/01_section_*.txt "$REPORT_DIR"/01_subsection_*.txt \
                    "$REPORT_DIR"/02_section_*.txt "$REPORT_DIR"/02_subsection_*.txt \
                    "$REPORT_DIR"/03_section_*.txt "$REPORT_DIR"/03_subsection_*.txt \
                    "$REPORT_DIR"/04_section_*.txt "$REPORT_DIR"/04_subsection_*.txt \
                    "$REPORT_DIR"/05_section_*.txt "$REPORT_DIR"/05_subsection_*.txt \
                    "$REPORT_DIR"/06_*.txt \
                    "$REPORT_DIR"/99_*.txt; do
    if [ -f "$section_file" ]; then
        echo "Добавление: $section_file"
        cat "$section_file" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi
done

echo "✓ Отчёт собран: $OUTPUT_FILE"