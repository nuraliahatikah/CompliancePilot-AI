const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: "admin" | "compliance_officer" | "auditor";
  is_active: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface Document {
  id: number;
  title: string;
  filename: string;
  file_type: string;
  file_size: number;
  document_type: string;
  status: string;
  ocr_used: boolean;
  owner_id: number;
  created_at: string;
  updated_at: string;
  has_analysis: boolean;
  risk_score: number | null;
  risk_level: string | null;
}

export interface Finding {
  category: string;
  severity: string;
  title: string;
  description: string;
  regulation_reference?: string;
  clause_excerpt?: string;
}

export interface Analysis {
  id: number;
  document_id: number;
  risk_score: number;
  risk_level: string;
  summary: string;
  findings: Finding[];
  recommendations: string[];
  compliance_gaps: string[];
  agent_outputs: Record<string, unknown>;
  rag_sources: Array<{
    content: string;
    source: string;
    regulation: string;
    section: string;
    relevance_score: number;
  }>;
  processing_time_seconds: number;
  created_at: string;
}

export interface DocumentDetail extends Document {
  extracted_text: string | null;
  analysis: Analysis | null;
}

export interface DashboardStats {
  total_documents: number;
  completed_analyses: number;
  pending_documents: number;
  average_risk_score: number;
  risk_distribution: Record<string, number>;
  recent_documents: Document[];
  documents_by_type: Record<string, number>;
  analyses_this_week: number;
}

export interface KnowledgeBaseResult {
  content: string;
  source: string;
  regulation: string;
  section: string;
  relevance_score: number;
}

export interface Report {
  id: number;
  document_id: number;
  title: string;
  file_path: string;
  created_at: string;
  download_url: string | null;
}

class ApiClient {
  private getToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("cp_token");
  }

  setToken(token: string): void {
    localStorage.setItem("cp_token", token);
  }

  clearToken(): void {
    localStorage.removeItem("cp_token");
    localStorage.removeItem("cp_user");
  }

  setUser(user: User): void {
    localStorage.setItem("cp_user", JSON.stringify(user));
  }

  getUser(): User | null {
    if (typeof window === "undefined") return null;
    const raw = localStorage.getItem("cp_user");
    return raw ? JSON.parse(raw) : null;
  }

  private async request<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken();
    const headers: Record<string, string> = {
      ...(options.headers as Record<string, string>),
    };

    if (!(options.body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
    }

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      this.clearToken();
      if (typeof window !== "undefined" && !window.location.pathname.includes("/login")) {
        window.location.href = "/login";
      }
      throw new Error("Unauthorized");
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Request failed" }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    if (response.status === 204) return {} as T;
    return response.json();
  }

  async login(email: string, password: string): Promise<TokenResponse> {
    return this.request<TokenResponse>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  }

  async register(data: {
    email: string;
    password: string;
    full_name: string;
    role?: string;
  }): Promise<User> {
    return this.request<User>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getMe(): Promise<User> {
    return this.request<User>("/api/auth/me");
  }

  async logout(): Promise<void> {
    await this.request("/api/auth/logout", { method: "POST" });
    this.clearToken();
  }

  async getDashboard(): Promise<DashboardStats> {
    return this.request<DashboardStats>("/api/admin/dashboard");
  }

  async getDocuments(): Promise<Document[]> {
    return this.request<Document[]>("/api/documents/");
  }

  async getDocument(id: number): Promise<DocumentDetail> {
    return this.request<DocumentDetail>(`/api/documents/${id}`);
  }

  async uploadDocument(file: File, title: string, documentType: string): Promise<Document> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("title", title);
    formData.append("document_type", documentType);
    return this.request<Document>("/api/documents/upload", {
      method: "POST",
      body: formData,
    });
  }

  async deleteDocument(id: number): Promise<void> {
    await this.request(`/api/documents/${id}`, { method: "DELETE" });
  }

  async analyzeDocument(id: number, forceReanalyze = false): Promise<Analysis> {
    return this.request<Analysis>(`/api/ai/analyze/${id}`, {
      method: "POST",
      body: JSON.stringify({ force_reanalyze: forceReanalyze }),
    });
  }

  async getAnalysis(documentId: number): Promise<Analysis> {
    return this.request<Analysis>(`/api/ai/analysis/${documentId}`);
  }

  async queryKnowledgeBase(query: string, topK = 5): Promise<{
    query: string;
    results: KnowledgeBaseResult[];
    total_results: number;
  }> {
    return this.request("/api/ai/knowledge-base/query", {
      method: "POST",
      body: JSON.stringify({ query, top_k: topK }),
    });
  }

  async getRegulations(): Promise<{
    regulations: Array<{ regulation: string; section: string; source: string; content: string }>;
    stats: Record<string, unknown>;
  }> {
    return this.request("/api/ai/knowledge-base/regulations");
  }

  async generateReport(documentId: number): Promise<Report> {
    return this.request<Report>(`/api/reports/generate/${documentId}`, {
      method: "POST",
    });
  }

  async getReports(): Promise<Report[]> {
    return this.request<Report[]>("/api/reports/");
  }

  getReportDownloadUrl(reportId: number): string {
    return `${API_URL}/api/reports/${reportId}/download`;
  }

  async downloadReport(reportId: number): Promise<void> {
    const token = this.getToken();
    const response = await fetch(this.getReportDownloadUrl(reportId), {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!response.ok) throw new Error("Download failed");
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `compliance_report_${reportId}.pdf`;
    a.click();
    window.URL.revokeObjectURL(url);
  }
}

export const api = new ApiClient();
