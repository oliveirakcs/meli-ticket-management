import React, { useState } from "react";
import { Category, CategoryCreation } from "../types/generalTypes";

interface CategoryModalProps {
  category: Category | null;
  isEditMode: boolean;
  onClose: () => void;
  onSubmit: (category: Category | CategoryCreation) => void;
}

const CategoryModal: React.FC<CategoryModalProps> = ({
  category,
  isEditMode,
  onClose,
  onSubmit,
}) => {
  const [name, setName] = useState(category?.name || "");

  const handleSubmit = () => {
    if (name.trim() === "") {
      alert("O nome da categoria é obrigatório.");
      return;
    }

    const newCategory = {
      ...(isEditMode ? { id: category?.id } : {}),
      name,
    };

    onSubmit(newCategory as Category | CategoryCreation);
    onClose();
  };

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1000,
      }}
    >
      <div
        style={{
          backgroundColor: "white",
          padding: "20px",
          borderRadius: "8px",
          width: "400px",
          maxWidth: "calc(100% - 40px)",
          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
          textAlign: "center",
          boxSizing: "border-box",
        }}
      >
        <h2>{isEditMode ? "Editar Categoria" : "Criar Categoria"}</h2>
        <input
          type="text"
          placeholder="Nome da Categoria"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "20px",
            borderRadius: "4px",
            border: "1px solid #ccc",
            outline: "none",
            fontSize: "16px",
            boxSizing: "border-box",
          }}
        />
        <button
          onClick={handleSubmit}
          style={{
            backgroundColor: "#007bff",
            border: "none",
            padding: "10px 20px",
            borderRadius: "5px",
            color: "white",
            cursor: "pointer",
            transition: "background-color 0.3s ease",
            fontSize: "16px",
            boxShadow: "0 2px 4px rgba(0, 0, 0, 0.2)",
            outline: "none",
            marginRight: "10px",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.backgroundColor = "#0056b3")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.backgroundColor = "#007bff")
          }
        >
          {isEditMode ? "Atualizar" : "Criar"}
        </button>
        <button
          onClick={onClose}
          style={{
            backgroundColor: "#f44336",
            border: "none",
            padding: "10px 20px",
            borderRadius: "5px",
            color: "white",
            cursor: "pointer",
            transition: "background-color 0.3s ease",
            fontSize: "16px",
            boxShadow: "0 2px 4px rgba(0, 0, 0, 0.2)",
            outline: "none",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.backgroundColor = "#d32f2f")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.backgroundColor = "#f44336")
          }
        >
          Cancelar
        </button>
      </div>
    </div>
  );
};

export default CategoryModal;
