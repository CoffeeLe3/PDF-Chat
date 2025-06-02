"use client";
import axios from "axios";
import { useState } from "react";

const UploadPdf = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected && selected.type === "application/pdf") {
      setFile(selected);
      setMessage("");
    } else {
      setFile(null);
      alert("Please select a valid PDF file.");
    }
  };

  const uploadFile = async () => {
    if (!file) return;

    try {
      const res = await axios.get(`/api/get-upload-url?filename=${file.name}`);
      const { upload_url } = res.data;

      const uploadResult = await axios.put(upload_url, file, {
        headers: {
          "Content-Type": "application/pdf",
        },
      });

      const data = await fetch(`api/notify-uploaded`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ filename: file.name }),
      })

    } catch (err) {
      console.error(err);
      setMessage("Something went wrong.");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-4 bg-gray-800 rounded shadow">
      <h2 className="text-center text-green-200 text-xl font-semibold mb-4">
        Upload PDF
      </h2>

      <input
        type="file"
        accept="application/pdf"
        onChange={handleFileChange}
        className="mb-4 w-full"
      />

      <button
        onClick={uploadFile}
        className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded w-full"
      >
        Upload
      </button>

      {message && (
        <p className="mt-4 text-center text-sm text-yellow-200">{message}</p>
      )}
    </div>
  );
};

export default UploadPdf;
