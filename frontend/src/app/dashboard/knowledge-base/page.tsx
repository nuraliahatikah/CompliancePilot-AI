"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { BookOpen, Loader2, Search } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { api, type KnowledgeBaseResult } from "@/lib/api";

interface Regulation {
  regulation: string;
  section: string;
  source: string;
  content: string;
}

export default function KnowledgeBasePage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<KnowledgeBaseResult[]>([]);
  const [regulations, setRegulations] = useState<Regulation[]>([]);
  const [stats, setStats] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  useEffect(() => {
    api.getRegulations().then((data) => {
      setRegulations(data.regulations);
      setStats(data.stats);
    });
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim().length < 3) return;

    setLoading(true);
    setSearched(true);
    try {
      const data = await api.queryKnowledgeBase(query.trim());
      setResults(data.results);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const employmentRegs = regulations.filter((r) => r.regulation.includes("Employment"));
  const pdpaRegs = regulations.filter((r) => r.regulation.includes("Data Protection"));

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <BookOpen className="h-6 w-6" />
          Knowledge Base
        </h2>
        <p className="text-muted-foreground mt-1">
          ChromaDB vector search over Malaysian Employment Act 1955 and PDPA 2010
        </p>
      </div>

      {stats && (
        <div className="flex flex-wrap gap-3">
          <Badge variant="outline">{String(stats.total_documents)} regulations indexed</Badge>
          <Badge variant="outline">Backend: {String(stats.backend)}</Badge>
          <Badge variant="secondary">Employment Act 1955</Badge>
          <Badge variant="secondary">PDPA 2010</Badge>
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Semantic Search</CardTitle>
          <CardDescription>
            Query the RAG knowledge base for relevant Malaysian regulations
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSearch} className="flex gap-3">
            <Input
              placeholder="e.g. overtime working hours employment contract termination notice"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="flex-1"
            />
            <Button type="submit" disabled={loading || query.trim().length < 3}>
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
              Search
            </Button>
          </form>
        </CardContent>
      </Card>

      {searched && (
        <div className="space-y-4">
          <h3 className="font-semibold">
            Search Results {results.length > 0 && `(${results.length})`}
          </h3>
          {results.length === 0 ? (
            <Card>
              <CardContent className="py-8 text-center text-muted-foreground">
                No matching regulations found. Try different keywords.
              </CardContent>
            </Card>
          ) : (
            results.map((result, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <Card>
                  <CardHeader className="pb-2">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-base">{result.section}</CardTitle>
                      <Badge variant="outline">
                        {(result.relevance_score * 100).toFixed(0)}% relevant
                      </Badge>
                    </div>
                    <CardDescription>
                      {result.regulation} · {result.source}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm leading-relaxed">{result.content}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))
          )}
        </div>
      )}

      <Tabs defaultValue="employment">
        <TabsList>
          <TabsTrigger value="employment">Employment Act 1955</TabsTrigger>
          <TabsTrigger value="pdpa">PDPA 2010</TabsTrigger>
        </TabsList>

        <TabsContent value="employment" className="mt-4">
          <ScrollArea className="h-[500px]">
            <div className="space-y-4 pr-4">
              {employmentRegs.map((reg, i) => (
                <Card key={i}>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm">{reg.section}</CardTitle>
                    <CardDescription>{reg.source}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">{reg.content}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="pdpa" className="mt-4">
          <ScrollArea className="h-[500px]">
            <div className="space-y-4 pr-4">
              {pdpaRegs.map((reg, i) => (
                <Card key={i}>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm">{reg.section}</CardTitle>
                    <CardDescription>{reg.source}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">{reg.content}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </ScrollArea>
        </TabsContent>
      </Tabs>
    </div>
  );
}
