"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Brain,
  FileSearch,
  Scale,
  Shield,
  Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const features = [
  {
    icon: FileSearch,
    title: "Document Intelligence",
    description: "Upload contracts, policies, and business documents with automatic OCR extraction.",
  },
  {
    icon: Brain,
    title: "Multi-Agent AI Analysis",
    description: "CrewAI pipeline with legal analyst, risk assessor, and policy advisor agents.",
  },
  {
    icon: Scale,
    title: "Malaysian Compliance RAG",
    description: "Cross-reference against Employment Act 1955 and PDPA 2010 via ChromaDB vector search.",
  },
  {
    icon: Shield,
    title: "Audit-Ready Reports",
    description: "Download professional PDF compliance audit reports with findings and recommendations.",
  },
];

export default function HomePage() {
  return (
    <div className="min-h-screen">
      <header className="border-b bg-background/95 backdrop-blur sticky top-0 z-50">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary">
              <Shield className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="text-lg font-bold">CompliancePilot AI</span>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/login">
              <Button variant="ghost">Sign In</Button>
            </Link>
            <Link href="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      <section className="gradient-hero text-white">
        <div className="container mx-auto px-4 py-24 lg:py-32">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-3xl"
          >
            <div className="inline-flex items-center gap-2 rounded-full bg-white/10 px-4 py-1.5 text-sm mb-6">
              <Sparkles className="h-4 w-4" />
              AI-Powered Compliance Intelligence
            </div>
            <h1 className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
              Navigate Malaysian Compliance with Confidence
            </h1>
            <p className="mt-6 text-lg text-white/80 max-w-2xl">
              CompliancePilot AI ingests your contracts and policies, runs them through a
              multi-agent CrewAI pipeline, and cross-references Malaysian Employment Act 1955
              and PDPA regulations to deliver actionable risk scores and audit reports.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link href="/register">
                <Button size="lg" variant="secondary" className="gap-2">
                  Start Free Trial
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link href="/login">
                <Button size="lg" variant="outline" className="border-white/30 text-white hover:bg-white/10">
                  View Demo
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold">Enterprise-Ready Features</h2>
          <p className="mt-3 text-muted-foreground max-w-2xl mx-auto">
            Built for compliance officers, auditors, and administrators with role-based access control.
          </p>
        </div>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <Card className="h-full hover:shadow-lg transition-shadow">
                  <CardContent className="pt-6">
                    <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 mb-4">
                      <Icon className="h-6 w-6 text-primary" />
                    </div>
                    <h3 className="font-semibold text-lg">{feature.title}</h3>
                    <p className="mt-2 text-sm text-muted-foreground">{feature.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </section>

      <section className="border-t bg-muted/30">
        <div className="container mx-auto px-4 py-16 text-center">
          <h2 className="text-2xl font-bold">Ready for your hackathon demo?</h2>
          <p className="mt-2 text-muted-foreground">
            Register an account — the first user becomes Admin automatically.
          </p>
          <Link href="/register" className="inline-block mt-6">
            <Button size="lg">Create Account</Button>
          </Link>
        </div>
      </section>

      <footer className="border-t py-8">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} CompliancePilot AI. Built for Malaysian regulatory compliance.
        </div>
      </footer>
    </div>
  );
}
