import { useState } from "react";
import { BrainCircuit, Eye, EyeOff } from "lucide-react";

interface Props {
  title?: string | null;
  prompt: string;
  reveal?: string | null;
}

export function Prediction({ title, prompt, reveal }: Props) {
  const [shown, setShown] = useState(false);
  return (
    <section className="prediction-card">
      <header>
        <span className="prediction-icon"><BrainCircuit size={19} /></span>
        <div>
          <span className="eyebrow">Prediction checkpoint</span>
          <h2>{title ?? "Commit before you manipulate"}</h2>
        </div>
      </header>
      <p>{prompt}</p>
      {reveal ? (
        <>
          <button type="button" className="secondary-button" onClick={() => setShown((value) => !value)}>
            {shown ? <EyeOff size={16} /> : <Eye size={16} />}
            {shown ? "Hide answer" : "Reveal after predicting"}
          </button>
          {shown ? <div className="prediction-answer">{reveal}</div> : null}
        </>
      ) : null}
    </section>
  );
}
