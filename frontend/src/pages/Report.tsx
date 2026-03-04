import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Layout from "@/components/layout/Layout";
import LoadingSpinner from "@/components/LoadingSpinner";

const cleanText = (text: string) => {
  if (!text) return "";

  return text
    .replace(/\*\*/g, "")          // remove **
    .replace(/\\n/g, "\n")          // convert escaped newlines
    .replace(/"\s*}/g, "")          // cleanup JSON leftovers
    .trim();
};

const Report = () => {
  const { id } = useParams();
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/report/${id}`)
      .then((res) => res.json())
      .then((data) => {
        setReport(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center py-20">
          <LoadingSpinner size="lg" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto mt-8">
		  <div className="mt-6 rounded-xl bg-white/10 p-6 text-white backdrop-blur">
			  <h2 className="mb-4 text-xl font-semibold">AI Credit Report</h2>

			  <p className="whitespace-pre-line leading-relaxed text-white/90">
				{cleanText(report.ai_report)}
			  </p>
			</div>
		</div>
    </Layout>
  );
};

export default Report;
