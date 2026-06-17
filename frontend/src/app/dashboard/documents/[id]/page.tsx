"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { motion } from "framer-motion";
import {
  AlertTriangle,
  Brain,
  Download,
  FileText,
  Loader2,
  RefreshCw,
  Shield,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { api, type Analysis, type DocumentDetail } from "@/lib/api";
import { formatDate, formatFileSize, getRiskColor } from "@/lib/utils";

const STATUS_PROGRESS: Record<string, number> = {
  uploaded: 20,
  processing: 40,
  ocr_complete: 60,
  analyzing: 80,
  completed: 100,
  failed: 0,
};

export default function DocumentDetailPage() {
  const params = useParams();
  const documentId = Number(params.id);
  const [doc, setDoc] = useState<DocumentDetail | null>(null);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [generatingReport, setGeneratingReport] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const loadDocument = useCallback(async () => {
    try {
      const data = await api.getDocument(documentId);
      setDoc(data);
      setAnalysis(data.analysis);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load document");
    } finally {
      setLoading(false);
    }
  }, [documentId]);

  useEffect(() => {
    loadDocument();
  }, [loadDocument]);

  useEffect(() => {
    if (!doc || doc.status === "completed" || doc.status === "failed") return;

    const interval = setInterval(loadDocument, 3000);
    return () => clearInterval(interval);
  }, [doc, loadDocument]);

  const handleAnalyze = async (force = false) => {
    setAnalyzing(true);
    setMessage("");
    setError("");
    try {
      const result = await api.analyzeDocument(documentId, force);
      setAnalysis(result);
      await loadDocument();
      setMessage("Analysis completed successfully");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setAnalyzing(false);
    }
  };

  const handleGenerateReport = async () => {
    setGeneratingReport(true);
    setError("");
    try {
      const report = await api.generateReport(documentId);
      await api.downloadReport(report.id);
      setMessage("Report downloaded successfully");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Report generation failed");
    } finally {
      setGeneratingReport(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!doc) {
    return (
      <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-4 text-destructive">
        {error || "Document not found"}
      </div>
    );
  }

  const canAnalyze = doc.status === "ocr_complete" || doc.status === "completed";
  const progress = STATUS_PROGRESS[doc.status] ?? 0;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h2 className="text-2xl font-bold">{doc.title}</h2>
          <p className="text-muted-foreground mt-1">
            {doc.filename} · {formatFileSize(doc.file_size)} · {formatDate(doc.created_at)}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Badge variant="outline" className="capitalize">
            {doc.document_type}
          </Badge>
          <Badge variant="outline" className="capitalize">
            {doc.status.replace("_", " ")}
          </Badge>
          {doc.ocr_used && <Badge variant="secondary">OCR Applied</Badge>}
        </div>
      </div>

      {error && (
        <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">{error}</div>
      )}
      {message && (
        <div className="rounded-md bg-green-50 p-3 text-sm text-green-700">{message}</div>
      )}

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Processing Status</CardTitle>
        </CardHeader>
        <CardContent>
          <Progress value={progress} className="mb-2" />
          <p className="text-sm text-muted-foreground capitalize">
            {doc.status.replace("_", " ")} — {progress}% complete
          </p>
        </CardContent>
      </Card>

      <div className="flex flex-wrap gap-3">
        <Button
          onClick={() => handleAnalyze(!!analysis)}
          disabled={!canAnalyze || analyzing || doc.status === "processing"}
        >
          {analyzing ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Brain className="h-4 w-4" />
          )}
          {analysis ? "Re-analyze" : "Run AI Analysis"}
        </Button>
        {analysis && (
          <Button variant="outline" onClick={handleGenerateReport} disabled={generatingReport}>
            {generatingReport ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Download className="h-4 w-4" />
            )}
            Download PDF Report
          </Button>
        )}
        <Button variant="ghost" onClick={loadDocument}>
          <RefreshCw className="h-4 w-4" />
          Refresh
        </Button>
      </div>

      {analysis && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <Card className="border-2">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Risk Assessment</CardTitle>
                  <CardDescription>
                    Processed in {analysis.processing_time_seconds}s via{" "}
                    {(analysis.agent_outputs?.pipeline as string) || "AI pipeline"}
                  </CardDescription>
                </div>
                <div className={`rounded-xl border px-4 py-2 text-center ${getRiskColor(analysis.risk_level)}`}>
                  <div className="text-2xl font-bold">{analysis.risk_score.toFixed(0)}</div>
                  <div className="text-xs uppercase font-medium">{analysis.risk_level}</div>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm leading-relaxed">{analysis.summary}</p>
            </CardContent>
          </Card>
        </motion.div>
      )}

      <Tabs defaultValue="findings">
        <TabsList>
          <TabsTrigger value="findings">Findings</TabsTrigger>
          <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
          <TabsTrigger value="rag">RAG Sources</TabsTrigger>
          <TabsTrigger value="text">Extracted Text</TabsTrigger>
        </TabsList>

        <TabsContent value="findings" className="mt-4">
          {!analysis ? (
            <Card>
              <CardContent className="py-12 text-center text-muted-foreground">
                <AlertTriangle className="mx-auto h-8 w-8 mb-3" />
                Run AI analysis to view compliance findings
              </CardContent>
            </Card>
          ) : analysis.findings.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center">
                <Shield className="mx-auto h-8 w-8 mb-3 text-green-600" />
                <p className="font-medium">No significant compliance issues detected</p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              {analysis.findings.map((finding, i) => (
                <Card key={i}>
                  <CardHeader className="pb-2">
                    <div className="flex items-start justify-between gap-4">
                      <CardTitle className="text-base">{finding.title}</CardTitle>
                      <Badge
                        variant={finding.severity === "high" || finding.severity === "critical" ? "destructive" : "secondary"}
                        className="capitalize shrink-0"
                      >
                        {finding.severity}
                      </Badge>
                    </div>
                    <CardDescription>{finding.category}</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <p className="text-sm">{finding.description}</p>
                    {finding.regulation_reference && (
                      <p className="text-xs text-muted-foreground">
                        Reference: {finding.regulation_reference}
                      </p>
                    )}
                    {finding.clause_excerpt && (
                      <blockquote className="border-l-2 pl-3 text-xs text-muted-foreground italic">
                        &ldquo;{finding.clause_excerpt}&rdquo;
                      </blockquote>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="recommendations" className="mt-4">
          <Card>
            <CardContent className="pt-6">
              {!analysis ? (
                <p className="text-center text-muted-foreground py-8">No recommendations yet</p>
              ) : (
                <ol className="space-y-3">
                  {analysis.recommendations.map((rec, i) => (
                    <li key={i} className="flex gap-3 text-sm">
                      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-bold">
                        {i + 1}
                      </span>
                      {rec}
                    </li>
                  ))}
                </ol>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="rag" className="mt-4">
          <div className="space-y-4">
            {!analysis?.rag_sources?.length ? (
              <Card>
                <CardContent className="py-12 text-center text-muted-foreground">
                  RAG sources will appear after analysis
                </CardContent>
              </Card>
            ) : (
              analysis.rag_sources.map((source, i) => (
                <Card key={i}>
                  <CardHeader className="pb-2">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-sm">{source.section}</CardTitle>
                      <Badge variant="outline">
                        {(source.relevance_score * 100).toFixed(0)}% match
                      </Badge>
                    </div>
                    <CardDescription>{source.regulation}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">{source.content}</p>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </TabsContent>

        <TabsContent value="text" className="mt-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <FileText className="h-4 w-4" />
                Extracted Document Text
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-[400px] rounded-md border p-4">
                <pre className="whitespace-pre-wrap text-xs font-mono">
                  {doc.extracted_text || "Text extraction in progress..."}
                </pre>
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {analysis?.compliance_gaps && analysis.compliance_gaps.length > 0 && (
        <>
          <Separator />
          <Card className="border-amber-200 bg-amber-50/50">
            <CardHeader>
              <CardTitle className="text-base text-amber-800">Compliance Gaps</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {analysis.compliance_gaps.map((gap, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-amber-900">
                    <AlertTriangle className="h-4 w-4 shrink-0 mt-0.5" />
                    {gap}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
