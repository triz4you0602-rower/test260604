"""
Generate visual diagrams for Streamlit + Supabase project
Creates flow diagrams, architecture charts, and timeline visualizations
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from datetime import datetime

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = {
    'local': '#4E79A7',      # Blue (Local development)
    'supabase': '#F28E2B',   # Orange (Cloud)
    'csv': '#59A14F',        # Green (CSV)
    'deploy': '#E15759',     # Red (Deployment)
    'success': '#70AD47',    # Light Green (Success)
    'warning': '#FFD966'     # Yellow (Warning)
}

def create_architecture_diagram():
    """Create system architecture diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, 'Streamlit + Supabase 시스템 아키텍처',
            fontsize=20, fontweight='bold', ha='center', family='DejaVu Sans')

    # User Layer
    user_box = FancyBboxPatch((3.5, 8), 3, 0.6,
                              boxstyle="round,pad=0.1",
                              edgecolor='black', facecolor='#E7E6E6', linewidth=2)
    ax.add_patch(user_box)
    ax.text(5, 8.3, '👥 사용자 (Web Browser)', ha='center', fontsize=11, fontweight='bold')

    # Arrow down
    arrow1 = FancyArrowPatch((5, 8), (5, 7.3),
                            arrowstyle='->', mutation_scale=30, linewidth=2, color='black')
    ax.add_patch(arrow1)

    # Streamlit Layer
    streamlit_box = FancyBboxPatch((2, 6), 6, 1,
                                   boxstyle="round,pad=0.1",
                                   edgecolor='black', facecolor=colors['local'],
                                   linewidth=2, alpha=0.7)
    ax.add_patch(streamlit_box)
    ax.text(5, 6.8, 'Streamlit 앱', ha='center', fontsize=12, fontweight='bold', color='white')
    ax.text(5, 6.4, '로컬: http://localhost:8501', ha='center', fontsize=9, color='white')
    ax.text(5, 6.1, '배포: https://test260604-pcyo6o9...streamlit.app/', ha='center', fontsize=8, color='white')

    # Arrows down
    arrow2a = FancyArrowPatch((3.5, 6), (2.5, 4.8),
                             arrowstyle='->', mutation_scale=25, linewidth=2.5, color=colors['supabase'])
    arrow2b = FancyArrowPatch((6.5, 6), (7.5, 4.8),
                             arrowstyle='->', mutation_scale=25, linewidth=2.5, color=colors['csv'])
    ax.add_patch(arrow2a)
    ax.add_patch(arrow2b)

    # Data Sources
    # Supabase
    supabase_box = FancyBboxPatch((0.5, 3.5), 4, 1.2,
                                  boxstyle="round,pad=0.1",
                                  edgecolor='black', facecolor=colors['supabase'],
                                  linewidth=2, alpha=0.7)
    ax.add_patch(supabase_box)
    ax.text(2.5, 4.4, '☁️ Supabase (Cloud DB)', ha='center', fontsize=11, fontweight='bold', color='white')
    ax.text(2.5, 4, '• PostgreSQL', ha='center', fontsize=8, color='white')
    ax.text(2.5, 3.7, '• 151개 행', ha='center', fontsize=8, color='white')

    # CSV
    csv_box = FancyBboxPatch((5.5, 3.5), 4, 1.2,
                             boxstyle="round,pad=0.1",
                             edgecolor='black', facecolor=colors['csv'],
                             linewidth=2, alpha=0.7)
    ax.add_patch(csv_box)
    ax.text(7.5, 4.4, '📄 CSV 파일 (로컬)', ha='center', fontsize=11, fontweight='bold', color='white')
    ax.text(7.5, 4, '• 로컬 저장소', ha='center', fontsize=8, color='white')
    ax.text(7.5, 3.7, '• 150개 행', ha='center', fontsize=8, color='white')

    # Arrow with label
    ax.text(3.2, 5.2, '우선', fontsize=9, style='italic', color=colors['supabase'], fontweight='bold')
    ax.text(7, 5.2, '폴백', fontsize=9, style='italic', color=colors['csv'], fontweight='bold')

    # Data Flow Box
    data_box = FancyBboxPatch((1.5, 1.5), 7, 1.8,
                              boxstyle="round,pad=0.1",
                              edgecolor='black', facecolor='#F0F0F0',
                              linewidth=2, linestyle='--')
    ax.add_patch(data_box)
    ax.text(5, 3, '📊 최종 사용자 보기 (대시보드)', ha='center', fontsize=11, fontweight='bold')

    ax.text(5, 2.5, '✅ 메트릭 카드 (오늘, 어제, 증감률)', ha='center', fontsize=9)
    ax.text(5, 2.1, '📈 라인 차트 (일별 매출 추이)  |  🥧 파이 차트 (카테고리별 비중)', ha='center', fontsize=9)
    ax.text(5, 1.7, '⚡ 실시간 업데이트 (Supabase 변경사항 즉시 반영)', ha='center', fontsize=8, style='italic')

    # Arrows to dashboard
    arrow3a = FancyArrowPatch((2.5, 3.5), (4, 3.3),
                             arrowstyle='->', mutation_scale=20, linewidth=2, color=colors['supabase'])
    arrow3b = FancyArrowPatch((7.5, 3.5), (6, 3.3),
                             arrowstyle='->', mutation_scale=20, linewidth=2, color=colors['csv'])
    ax.add_patch(arrow3a)
    ax.add_patch(arrow3b)

    # Legend
    ax.text(0.5, 0.8, '✨ 특징:', fontsize=10, fontweight='bold')
    ax.text(0.5, 0.4, '• 이중 안전 시스템 (Supabase + CSV)', fontsize=8)
    ax.text(0.5, 0.05, '• 실시간 데이터 동기화', fontsize=8)
    ax.text(5.5, 0.4, '• 자동 폴백 메커니즘', fontsize=8)
    ax.text(5.5, 0.05, '• 로컬 + 클라우드 배포 지원', fontsize=8)

    plt.tight_layout()
    plt.savefig('C:\\test01\\diagram_architecture.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Architecture diagram saved: diagram_architecture.png")
    plt.close()

def create_workflow_timeline():
    """Create project timeline/workflow diagram"""
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, '프로젝트 워크플로우 타임라인',
            fontsize=20, fontweight='bold', ha='center', family='DejaVu Sans')

    # Timeline
    phases = [
        {'day': 1, 'title': '초기 설정', 'tasks': ['프로젝트 생성', '패키지 설정', '앱 개발'], 'x': 1.5},
        {'day': 2, 'title': 'Supabase 연동', 'tasks': ['DB 생성', '테이블 구성', '로컬 연결'], 'x': 3.5},
        {'day': 3, 'title': '데이터 동기화', 'tasks': ['CSV 이전', '실시간 테스트', '검증'], 'x': 5.5},
        {'day': 4, 'title': '배포', 'tasks': ['Github 커밋', 'Cloud 배포', '권한 설정'], 'x': 7.5},
    ]

    # Draw phases
    for phase in phases:
        # Phase box
        box = FancyBboxPatch((phase['x']-0.7, 6.5), 1.4, 2.2,
                            boxstyle="round,pad=0.1",
                            edgecolor='black',
                            facecolor=colors['local'] if phase['day'] in [1,3] else colors['deploy'],
                            linewidth=2.5, alpha=0.7)
        ax.add_patch(box)

        # Day label
        ax.text(phase['x'], 8.4, f"Day {phase['day']}",
               ha='center', fontsize=11, fontweight='bold', color='white')

        # Title
        ax.text(phase['x'], 8, phase['title'],
               ha='center', fontsize=10, fontweight='bold', color='white')

        # Tasks
        for i, task in enumerate(phase['tasks']):
            ax.text(phase['x'], 7.5 - i*0.35, f"• {task}",
                   ha='center', fontsize=7, color='white')

        # Arrow to next phase
        if phase['day'] < 4:
            arrow = FancyArrowPatch((phase['x'] + 0.7, 7.6),
                                   (phase['x'] + 1.3, 7.6),
                                   arrowstyle='->', mutation_scale=25,
                                   linewidth=2.5, color='black')
            ax.add_patch(arrow)

    # Current status
    ax.text(5, 5.8, '📊 현재 상태: ✅ 완성 및 운영 중',
           ha='center', fontsize=12, fontweight='bold', color=colors['success'])

    # Key achievements
    achievements = [
        '✅ 로컬 앱: Supabase + CSV 완벽 동기화',
        '✅ 배포 앱: Supabase 실시간 연동 (권한 설정 완료)',
        '✅ 데이터: 151개 행 클라우드 저장',
        '✅ 자동 폴백: CSV 백업 시스템 작동',
        '✅ 문서: 설정 가이드 + 워크플로우 작성'
    ]

    y_pos = 5.2
    ax.text(0.5, 5.8, '🎯 주요 성과:', fontsize=11, fontweight='bold')
    for achievement in achievements:
        ax.text(0.7, y_pos, achievement, fontsize=9)
        y_pos -= 0.45

    # Test results
    ax.text(5.5, 5.8, '✨ 검증 완료:', fontsize=11, fontweight='bold')
    tests = [
        '✅ 실시간 동기화 테스트 성공',
        '✅ 메트릭 정확성 검증',
        '✅ 차트 렌더링 확인',
        '✅ 배포 앱 권한 설정 완료',
        '✅ 폴백 메커니즘 작동 확인'
    ]

    y_pos = 5.2
    for test in tests:
        ax.text(5.7, y_pos, test, fontsize=9)
        y_pos -= 0.45

    # Metrics box
    metrics_box = FancyBboxPatch((1, 0.2), 8, 1.5,
                                boxstyle="round,pad=0.1",
                                edgecolor='black',
                                facecolor='#E7E6E6',
                                linewidth=2)
    ax.add_patch(metrics_box)

    ax.text(5, 1.5, '📈 최종 메트릭', ha='center', fontsize=11, fontweight='bold')
    ax.text(2, 0.9, '로컬 앱: 어제 ₩103.8M', ha='center', fontsize=9)
    ax.text(5, 0.9, '배포 앱: 어제 ₩103.8M', ha='center', fontsize=9)
    ax.text(8, 0.9, '증감률: +35.1%', ha='center', fontsize=9)
    ax.text(5, 0.4, '📊 데이터 정합성: 100% (Supabase ↔ 배포 앱)', ha='center', fontsize=8, style='italic')

    plt.tight_layout()
    plt.savefig('C:\\test01\\diagram_timeline.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Timeline diagram saved: diagram_timeline.png")
    plt.close()

def create_data_flow_diagram():
    """Create data flow diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, '데이터 흐름 및 동기화 메커니즘',
            fontsize=20, fontweight='bold', ha='center', family='DejaVu Sans')

    # CSV Source
    csv_source = FancyBboxPatch((0.5, 7.5), 2.5, 1,
                               boxstyle="round,pad=0.1",
                               edgecolor='black', facecolor=colors['csv'],
                               linewidth=2.5, alpha=0.8)
    ax.add_patch(csv_source)
    ax.text(1.75, 8.2, '📄 CSV 파일', ha='center', fontsize=11, fontweight='bold', color='white')
    ax.text(1.75, 7.8, '150 rows', ha='center', fontsize=9, color='white')

    # Arrow to migration
    arrow1 = FancyArrowPatch((3, 8), (4.2, 8),
                           arrowstyle='->', mutation_scale=25, linewidth=2.5, color=colors['success'])
    ax.add_patch(arrow1)
    ax.text(3.6, 8.3, '이전', fontsize=9, fontweight='bold', color=colors['success'])

    # Supabase
    supabase_db = FancyBboxPatch((4.2, 7.5), 2.5, 1,
                                boxstyle="round,pad=0.1",
                                edgecolor='black', facecolor=colors['supabase'],
                                linewidth=2.5, alpha=0.8)
    ax.add_patch(supabase_db)
    ax.text(5.45, 8.2, '☁️ Supabase DB', ha='center', fontsize=11, fontweight='bold', color='white')
    ax.text(5.45, 7.8, '151 rows', ha='center', fontsize=9, color='white')

    # Arrow to Streamlit
    arrow2 = FancyArrowPatch((5.45, 7.5), (5.45, 6.5),
                           arrowstyle='->', mutation_scale=30, linewidth=3, color=colors['success'])
    ax.add_patch(arrow2)
    ax.text(6.2, 7, '실시간\n연결', fontsize=9, fontweight='bold', color=colors['success'])

    # Streamlit App
    streamlit_app = FancyBboxPatch((3.5, 5.5), 3.9, 0.9,
                                  boxstyle="round,pad=0.1",
                                  edgecolor='black', facecolor=colors['local'],
                                  linewidth=2.5, alpha=0.8)
    ax.add_patch(streamlit_app)
    ax.text(5.45, 6.1, '🚀 Streamlit App', ha='center', fontsize=11, fontweight='bold', color='white')
    ax.text(5.45, 5.7, '(로컬 + 배포)', ha='center', fontsize=8, color='white')

    # Split for local and cloud
    # Local branch
    arrow3a = FancyArrowPatch((4, 5.5), (2.5, 4),
                            arrowstyle='->', mutation_scale=25, linewidth=2, color=colors['local'], linestyle='--')
    ax.add_patch(arrow3a)
    ax.text(3, 4.8, '로컬', fontsize=8, color=colors['local'])

    local_dashboard = FancyBboxPatch((0.8, 2.5), 3.4, 1.2,
                                    boxstyle="round,pad=0.1",
                                    edgecolor='black', facecolor=colors['local'],
                                    linewidth=2.5, alpha=0.7)
    ax.add_patch(local_dashboard)
    ax.text(2.5, 3.4, '💻 로컬 대시보드', ha='center', fontsize=10, fontweight='bold', color='white')
    ax.text(2.5, 2.95, 'http://localhost:8501', ha='center', fontsize=8, color='white')

    # Cloud branch
    arrow3b = FancyArrowPatch((6.9, 5.5), (8.5, 4),
                            arrowstyle='->', mutation_scale=25, linewidth=2, color=colors['deploy'], linestyle='--')
    ax.add_patch(arrow3b)
    ax.text(8, 4.8, '배포', fontsize=8, color=colors['deploy'])

    cloud_dashboard = FancyBboxPatch((5.8, 2.5), 3.4, 1.2,
                                   boxstyle="round,pad=0.1",
                                   edgecolor='black', facecolor=colors['deploy'],
                                   linewidth=2.5, alpha=0.7)
    ax.add_patch(cloud_dashboard)
    ax.text(7.5, 3.4, '☁️ 배포 대시보드', ha='center', fontsize=10, fontweight='bold', color='white')
    ax.text(7.5, 2.95, 'streamlit.app', ha='center', fontsize=8, color='white')

    # Arrows back to users
    arrow4a = FancyArrowPatch((2.5, 2.5), (2.5, 1.2),
                            arrowstyle='->', mutation_scale=25, linewidth=2, color=colors['local'])
    arrow4b = FancyArrowPatch((7.5, 2.5), (7.5, 1.2),
                            arrowstyle='->', mutation_scale=25, linewidth=2, color=colors['deploy'])
    ax.add_patch(arrow4a)
    ax.add_patch(arrow4b)

    # Final output
    final_box = FancyBboxPatch((0.5, 0), 9, 1.1,
                              boxstyle="round,pad=0.1",
                              edgecolor='black', facecolor='#E7E6E6',
                              linewidth=2.5)
    ax.add_patch(final_box)
    ax.text(5, 0.8, '👥 사용자 (Web Browser)', ha='center', fontsize=11, fontweight='bold')
    ax.text(5, 0.35, '✨ 실시간 메트릭, 차트, 분석 데이터 표시', ha='center', fontsize=9, style='italic')

    # Legend
    ax.text(0.3, 9.2, '범례:', fontsize=10, fontweight='bold')
    ax.plot([0.3, 0.5], [8.9, 8.9], color=colors['success'], linewidth=2.5)
    ax.text(0.6, 8.85, '데이터 이전 (1회)', fontsize=8)
    ax.plot([0.3, 0.5], [8.5, 8.5], color=colors['local'], linewidth=2.5)
    ax.text(0.6, 8.45, '실시간 연결', fontsize=8)

    plt.tight_layout()
    plt.savefig('C:\\test01\\diagram_dataflow.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Data flow diagram saved: diagram_dataflow.png")
    plt.close()

def main():
    """Generate all diagrams"""
    print("\n📊 Generating project visualization diagrams...\n")

    create_architecture_diagram()
    create_workflow_timeline()
    create_data_flow_diagram()

    print("\n" + "="*60)
    print("✅ All diagrams generated successfully!")
    print("="*60)
    print("\n📁 Generated files:")
    print("  1. diagram_architecture.png - System architecture")
    print("  2. diagram_timeline.png - Project workflow timeline")
    print("  3. diagram_dataflow.png - Data flow diagram")
    print("\n💾 Location: C:\\test01\\")
    print("\n✨ These diagrams are ready to use in presentations or documentation!\n")

if __name__ == "__main__":
    main()
