import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { TrendingUp, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import Layout from "@/components/layout/Layout";
import LoadingSpinner from "@/components/LoadingSpinner";
import { submitLoanApplication } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

/* ---------------- TYPES ---------------- */
interface LoanApplicationForm {
  business_type: "Manufacturing" | "Trading" | "Services";
  years_in_operation: number;
  annual_revenue: number;
  monthly_cashflow: number;
  loan_amount_requested: number;
  credit_score: number;
  existing_loans: number;
  debt_to_income_ratio: number;
  collateral_value: number;
  repayment_history: "Good" | "Average" | "Poor";
}

const LoanApplication = () => {
  const navigate = useNavigate();
  const { toast } = useToast();

  const [isLoading, setIsLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [documentType, setDocumentType] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const [formData, setFormData] = useState<LoanApplicationForm>({
    business_type: "Manufacturing",
    years_in_operation: 0,
    annual_revenue: 0,
    monthly_cashflow: 0,
    loan_amount_requested: 0,
    credit_score: 600,
    existing_loans: 0,
    debt_to_income_ratio: 0.5,
    collateral_value: 0,
    repayment_history: "Good",
  });

  /* ---------------- INPUT HANDLER ---------------- */
  const handleInputChange = (
    field: keyof LoanApplicationForm,
    value: any
  ) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  /* ---------------- DOCUMENT UPLOAD ---------------- */
  const handleDocumentUpload = async () => {
    if (!documentType || !selectedFile) {
      toast({
        title: "Missing information",
        description: "Select a document type and file",
        variant: "destructive",
      });
      return;
    }

    const payload = new FormData();
    payload.append("file", selectedFile);
    payload.append("document_type", documentType);

    try {
      setUploadLoading(true);
      const res = await fetch("http://127.0.0.1:8000/upload-document", {
        method: "POST",
        body: payload,
      });

      if (!res.ok) throw new Error("Upload failed");

      const data = await res.json();
      const extracted = data.extracted_fields || {};

      setFormData((prev) => ({
        ...prev,
        ...(extracted.annual_revenue && { annual_revenue: extracted.annual_revenue }),
        ...(extracted.monthly_cashflow && { monthly_cashflow: extracted.monthly_cashflow }),
        ...(extracted.collateral_value && { collateral_value: extracted.collateral_value }),
        ...(extracted.existing_loans && { existing_loans: extracted.existing_loans }),
      }));

      toast({
        title: "Auto‑fill complete",
        description: "Please verify extracted values",
      });
    } catch {
      toast({
        title: "Upload failed",
        description: "Could not extract document data",
        variant: "destructive",
      });
    } finally {
      setUploadLoading(false);
    }
  };

  /* ---------------- SUBMIT ---------------- */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const result = await submitLoanApplication({
        ...formData,
        debt_to_income_ratio: Number(formData.debt_to_income_ratio),
      });

      navigate("/result", { state: result });
    } catch {
      toast({
        title: "Prediction failed",
        description: "Backend rejected the request",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  /* ---------------- UI ---------------- */
  return (
    <Layout>
      <div className="mx-auto max-w-2xl py-16">
        <Card className="rounded-2xl bg-white/10 backdrop-blur-xl border border-white/10 shadow-xl">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <TrendingUp className="h-5 w-5 text-indigo-400" />
              Loan Application
            </CardTitle>
            <CardDescription className="text-white/70">
              AI‑assisted credit evaluation
            </CardDescription>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">

              {/* DOCUMENT UPLOAD */}
              <div className="rounded-xl border border-white/10 p-5 bg-white/5 space-y-4">
                <h3 className="text-sm font-semibold text-white">
                  Upload Financial Document (Optional)
                </h3>

                <Select value={documentType} onValueChange={setDocumentType}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select document type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="bank_statement">Bank Statement</SelectItem>
                    <SelectItem value="profit_and_loss">Profit & Loss</SelectItem>
                    <SelectItem value="balance_sheet">Balance Sheet</SelectItem>
                  </SelectContent>
                </Select>

                <Input
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg"
                  onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                />

                <Button
                  type="button"
                  variant="secondary"
                  disabled={uploadLoading}
                  onClick={handleDocumentUpload}
                >
                  {uploadLoading ? "Extracting…" : "Upload & Auto‑Fill"}
                </Button>
              </div>

              {/* FORM FIELDS */}
              <div className="space-y-4">

                <Label className="text-white">Business Type</Label>
                <Select
                  value={formData.business_type}
                  onValueChange={(v) =>
                    handleInputChange("business_type", v)
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Manufacturing">Manufacturing</SelectItem>
                    <SelectItem value="Trading">Trading</SelectItem>
                    <SelectItem value="Services">Services</SelectItem>
                  </SelectContent>
                </Select>

                {[
                  ["Years in Operation", "years_in_operation"],
                  ["Annual Revenue (₹)", "annual_revenue"],
                  ["Monthly Cashflow (₹)", "monthly_cashflow"],
                  ["Loan Amount Requested (₹)", "loan_amount_requested"],
                  ["Credit Score", "credit_score"],
                  ["Existing Loans", "existing_loans"],
                  ["Debt‑to‑Income Ratio", "debt_to_income_ratio"],
                  ["Collateral Value (₹)", "collateral_value"],
                ].map(([label, field]) => (
                  <div key={field}>
                    <Label className="text-white">{label}</Label>
                    <Input
                      type="number"
                      value={(formData as any)[field]}
                      onChange={(e) =>
                        handleInputChange(field as any, Number(e.target.value))
                      }
                    />
                  </div>
                ))}

                <Label className="text-white">Repayment History</Label>
                <Select
                  value={formData.repayment_history}
                  onValueChange={(v) =>
                    handleInputChange("repayment_history", v)
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Good">Good</SelectItem>
                    <SelectItem value="Average">Average</SelectItem>
                    <SelectItem value="Poor">Poor</SelectItem>
                  </SelectContent>
                </Select>

              </div>

              <Button
                type="submit"
                disabled={isLoading}
                className="w-full rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white"
              >
                {isLoading ? (
                  <>
                    <LoadingSpinner size="sm" /> Processing…
                  </>
                ) : (
                  <>
                    Submit for Risk Evaluation
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </>
                )}
              </Button>

            </form>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
};

export default LoanApplication;


