# reports_screen.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
import plotly.io as pio
from database_manager_mysql import get_database

# Keep the same signals as before for compatibility
class ReportsScreen(QWidget):
    logout_signal = pyqtSignal()
    show_overview_signal = pyqtSignal()
    show_enrollees_signal = pyqtSignal()
    show_reports_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F5F7FA;")
        self.db = get_database()  # uses the existing database manager
        self.setup_ui()
        # initial load
        self.refresh_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header (simple)
        header = QFrame()
        header.setFixedHeight(90)
        header.setStyleSheet("background-color: white; border-bottom: 2px solid #E8E8E8;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(40, 10, 40, 10)

        title_container = QVBoxLayout()
        title = QLabel("Reports")
        title.setStyleSheet("color: #060C0B; font-size: 22px; font-weight: 600;")
        subtitle = QLabel("Interactive dashboards — click Refresh to pull latest data")
        subtitle.setStyleSheet("color: #666; font-size: 13px;")
        title_container.addWidget(title)
        title_container.addWidget(subtitle)
        h_layout.addLayout(title_container)
        h_layout.addStretch()

        logout_btn = QPushButton("⎋ Logout")
        logout_btn.setFixedSize(120, 45)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #4A9A87;
                border: 2px solid #5DBAA3;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover { background-color: #E8F4F2; }
        """)
        logout_btn.clicked.connect(self.logout_signal.emit)
        h_layout.addWidget(logout_btn)

        main_layout.addWidget(header)

        # Controls: Refresh button + placeholders
        controls = QWidget()
        controls.setStyleSheet("background-color: #F8F9FA;")
        c_layout = QHBoxLayout(controls)
        c_layout.setContentsMargins(50, 15, 50, 15)

        refresh_btn = QPushButton("🔄 Refresh Data")
        refresh_btn.setFixedHeight(40)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D9B84;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #35B499; }
        """)
        refresh_btn.clicked.connect(self.refresh_data)
        c_layout.addWidget(refresh_btn)
        c_layout.addStretch()

        # Small note
        # note = QLabel("Interactive charts powered by Plotly — zoom/hover/click legend.")
        # note.setStyleSheet("color: #777; font-size: 13px;")
        # c_layout.addWidget(note)

        main_layout.addWidget(controls)

        # Chart grid: 2x2 using two QWebEngineViews (left: status + track; right: grade + strand)
        grid = QFrame()
        grid_layout = QHBoxLayout(grid)
        grid_layout.setContentsMargins(40, 20, 40, 40)
        grid_layout.setSpacing(40)

        # Left column (vertical)
        left_col = QVBoxLayout()
        left_col.setSpacing(40)

        self.view_enrollment_status = QWebEngineView()
        self.view_enrollment_status.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        left_col.addWidget(self.card_wrapper("Enrollment Status", self.view_enrollment_status, height=450))

        self.view_track_dist = QWebEngineView()
        self.view_track_dist.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        left_col.addWidget(self.card_wrapper("Track Distribution", self.view_track_dist, height=450))

        grid_layout.addLayout(left_col, 1)

        # Right column (vertical)
        right_col = QVBoxLayout()
        right_col.setSpacing(40)

        self.view_grade_dist = QWebEngineView()
        self.view_grade_dist.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_col.addWidget(self.card_wrapper("Grade Level Distribution", self.view_grade_dist, height=450))

        self.view_strand_dist = QWebEngineView()
        self.view_strand_dist.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_col.addWidget(self.card_wrapper("Strand Distribution", self.view_strand_dist, height=450))

        grid_layout.addLayout(right_col, 1)

        main_layout.addWidget(grid)

        # Footer
        footer = QLabel("Enrollify - Your Gateway to Senior High Success")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #999; font-size: 13px; padding: 20px 0;")
        main_layout.addWidget(footer)

    def card_wrapper(self, title_text, web_view: QWebEngineView, height=360):
        """Wrap a QWebEngineView inside a styled card with title"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E8E8E8;
            }
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(25, 20, 25, 25)
        layout.setSpacing(15)

        title = QLabel(title_text)
        title.setStyleSheet("color: #060C0B; font-size: 18px; font-weight: 700;")
        layout.addWidget(title)

        # container for web view
        web_view.setMinimumHeight(height)
        layout.addWidget(web_view)

        return frame

    # -------------------------
    # Data fetching + chart generation
    # -------------------------
    def refresh_data(self):
        """Fetch data from database and render all charts"""
        try:
            stats = self.db.get_statistics()
        except Exception as e:
            print("Failed to fetch statistics:", e)
            stats = {
                'total_students': 0, 'enrolled': 0, 'pending': 0,
                'grade11': 0, 'grade12': 0, 'tracks': {}, 'total_revenue': 0
            }

        # Prepare data for charts
        # Enrollment status pie
        status_labels = ["Enrolled", "Pending"]
        status_values = [stats.get('enrolled', 0), stats.get('pending', 0)]
        fig_status = go.Figure(data=[go.Pie(labels=status_labels, values=status_values, hole=0.4,
                                            marker=dict(colors=['#0099FF', '#5DBAA3']),
                                            textfont=dict(size=14))])
        fig_status.update_layout(margin=dict(t=30, b=80, l=50, r=50),
                                 legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=12)),
                                 paper_bgcolor="white", plot_bgcolor="white",
                                 height=380, autosize=True)

        # Track distribution - bar chart (sort by count desc)
        tracks = stats.get('tracks', {}) or {}
        track_labels = list(tracks.keys()) if tracks else ["N/A"]
        track_values = list(tracks.values()) if tracks else [0]
        fig_track = go.Figure(data=[go.Bar(x=track_labels, y=track_values,
                                           marker_color=['#8B7EC8' for _ in track_labels],
                                           text=track_values, textposition='outside')])
        fig_track.update_layout(title_text="By Track", showlegend=False,
                                margin=dict(t=60, b=80, l=70, r=50),
                                paper_bgcolor="white", plot_bgcolor="white",
                                xaxis=dict(title=None, tickfont=dict(size=11)),
                                yaxis=dict(title=dict(text="Students", font=dict(size=12)), tickfont=dict(size=11)),
                                height=380, autosize=True)

        # Grade distribution - donut
        grade_labels = ["Grade 11", "Grade 12"]
        grade_values = [stats.get('grade11', 0), stats.get('grade12', 0)]
        fig_grade = go.Figure(data=[go.Pie(labels=grade_labels, values=grade_values, hole=0.45,
                                           marker=dict(colors=['#0099FF', '#5DBAA3']),
                                           textfont=dict(size=14))])
        fig_grade.update_layout(margin=dict(t=30, b=80, l=50, r=50),
                                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=12)),
                                paper_bgcolor="white", plot_bgcolor="white",
                                height=380, autosize=True)

        # Strand distribution - horizontal bar (if many strands, show top N)
        # We'll query the DB for strand counts using a direct SQL for better accuracy
        strands = self._get_strand_counts()
        if strands:
            strand_labels = [s for s, _ in strands]
            strand_values = [v for _, v in strands]
        else:
            strand_labels = ["N/A"]
            strand_values = [0]

        fig_strand = go.Figure(data=[go.Bar(x=strand_values, y=strand_labels, orientation='h',
                                           marker_color=['#F59E0B' for _ in strand_labels],
                                           text=strand_values, textposition='outside')])
        fig_strand.update_layout(margin=dict(t=40, b=80, l=150, r=60),
                                 xaxis=dict(title=dict(text="Students", font=dict(size=12)), tickfont=dict(size=11)),
                                 yaxis=dict(tickfont=dict(size=11)),
                                 paper_bgcolor="white", plot_bgcolor="white",
                                 height=380, autosize=True)

        # Render each figure into the corresponding QWebEngineView
        try:
            self._render_plot_in_view(fig_status, self.view_enrollment_status)
            self._render_plot_in_view(fig_track, self.view_track_dist)
            self._render_plot_in_view(fig_grade, self.view_grade_dist)
            self._render_plot_in_view(fig_strand, self.view_strand_dist)
        except Exception as e:
            print("Failed to render plots:", e)

    def _render_plot_in_view(self, fig, web_view: QWebEngineView):
        """Convert plotly fig to HTML and load into QWebEngineView"""
        # Use CDN plotly JS so HTML is small
        html_body = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
        # small wrapper to keep the card background consistent
        html = f"""
        <html>
          <head>
            <meta charset="utf-8"/>
            <style>
              body {{ margin:0; padding:0; background-color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; overflow: hidden; }}
              .chart-container {{ width: 100%; height: 100%; box-sizing:border-box; }}
            </style>
          </head>
          <body>
            <div class="chart-container">{html_body}</div>
          </body>
        </html>
        """
        web_view.setHtml(html)

    def _get_strand_counts(self, top_n=8):
        """Query DB for strand counts, return list of (strand, count) sorted desc"""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT IFNULL(strand, 'Unspecified') AS strand, COUNT(*) AS cnt
                FROM students
                GROUP BY IFNULL(strand, 'Unspecified')
                ORDER BY cnt DESC
                LIMIT ?
            """, (top_n,))
            rows = cur.fetchall()
            conn.close()
            # rows are tuples (strand, cnt)
            return [(r[0], r[1]) for r in rows]
        except Exception:
            # fallback to stats summary or empty
            return []

