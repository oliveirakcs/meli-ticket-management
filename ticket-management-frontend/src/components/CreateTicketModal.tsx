import React, { useState } from "react";
import { createTicket, fetchSeverities } from "../services/api";
import { Category, Subcategory, Severity } from "../types/generalTypes";
import SelectCategoryModal from "./SelectCategoryModal";

interface CreateTicketModalProps {
  onClose: () => void;
  onTicketCreated: () => void;
}

const CreateTicketModal: React.FC<CreateTicketModalProps> = ({
  onClose,
  onTicketCreated,
}) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [selectedCategories, setSelectedCategories] = useState<
    { category: Category; subcategories: Subcategory[] }[]
  >([]);
  const [severities, setSeverities] = useState<Severity[]>([]);
  const [selectedSeverity, setSelectedSeverity] = useState<string>("");
  const [isSelectCategoryModalOpen, setIsSelectCategoryModalOpen] =
    useState(false);
  const [hoveredCategoryId, setHoveredCategoryId] = useState<string | null>(
    null
  );

  React.useEffect(() => {
    const loadSeverities = async () => {
      try {
        const severityData = await fetchSeverities();
        setSeverities(severityData);
      } catch (error) {
        console.error("Erro ao buscar Severities:", error);
      }
    };

    loadSeverities();
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (
      !title ||
      !description ||
      !selectedSeverity ||
      selectedCategories.length === 0
    ) {
      alert("Preencha todos os campos obrigatórios.");
      return;
    }

    const categoryIds = selectedCategories.map((cat) => cat.category.id);
    const subcategoryIds = selectedCategories.flatMap((cat) =>
      cat.subcategories.map((sub) => sub.id)
    );

    const newTicket = {
      title,
      description,
      category_ids: categoryIds,
      subcategory_ids: subcategoryIds,
      severity_id: selectedSeverity,
      status: "aberto",
      comment: "",
      comment_user: "",
    };

    try {
      await createTicket(newTicket);
      alert("Ticket criado com sucesso!");
      onTicketCreated();
      onClose();
    } catch (error: any) {
      if (
        error.response &&
        error.response.status === 400 &&
        error.response.data.detail ===
          "Cannot create a ticket with severity level 1."
      ) {
        alert(
          "Nos casos que são muito urgentes, como severidade nível 1, entre em contato com a equipe de suporte de emergência."
        );
      } else {
        console.error("Erro ao criar ticket:", error);
        alert(
          "Nos casos que são muito urgentes, como severidade nível 1, entre em contato com a equipe de suporte de emergência."
        );
      }
    }
  };

  const handleAddCategory = (
    category: Category,
    subcategories: Subcategory[]
  ) => {
    setSelectedCategories((prev) => [...prev, { category, subcategories }]);
  };

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
    >
      <div
        style={{
          backgroundColor: "#fff",
          padding: "40px",
          borderRadius: "8px",
          boxShadow: "0 2px 10px rgba(0, 0, 0, 0.2)",
          maxWidth: "500px",
          width: "90%",
        }}
      >
        <h2 style={{ marginBottom: "20px" }}>Criar Novo Ticket</h2>
        <form
          onSubmit={handleSubmit}
          style={{
            width: "100%",
          }}
        >
          <div style={{ marginBottom: "20px" }}>
            <label
              style={{
                display: "block",
                fontWeight: "bold",
                marginBottom: "8px",
                color: "#333",
              }}
            >
              Título:
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              style={{
                width: "100%",
                padding: "8px",
                borderRadius: "4px",
                border: "1px solid #ccc",
                boxSizing: "border-box",
              }}
            />
          </div>
          <div style={{ marginBottom: "20px" }}>
            <label
              style={{
                display: "block",
                fontWeight: "bold",
                marginBottom: "8px",
                color: "#333",
              }}
            >
              Descrição:
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              style={{
                width: "100%",
                padding: "8px",
                borderRadius: "4px",
                border: "1px solid #ccc",
                boxSizing: "border-box",
                resize: "vertical",
              }}
            />
          </div>
          <div style={{ marginBottom: "20px" }}>
            <button
              type="button"
              onClick={() => setIsSelectCategoryModalOpen(true)}
              style={{
                backgroundColor: "#007bff",
                color: "white",
                padding: "10px 20px",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
                transition: "background-color 0.3s ease",
                marginLeft: "auto",
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.backgroundColor = "#0056b3")
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.backgroundColor = "#007bff")
              }
            >
              Adicionar Categoria
            </button>
            {selectedCategories.length > 0 && (
              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: "10px",
                  marginTop: "10px",
                }}
              >
                {selectedCategories.map(({ category, subcategories }) => (
                  <div
                    key={category.id}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      padding: "10px",
                      backgroundColor: "#e9ecef",
                      border: "1px solid #ccc",
                      borderRadius: "5px",
                      position: "relative",
                      transition: "box-shadow 0.3s ease",
                    }}
                    onMouseEnter={() => setHoveredCategoryId(category.id)}
                    onMouseLeave={() => setHoveredCategoryId(null)}
                  >
                    <span
                      style={{
                        flex: 1,
                        marginRight: "10px",
                        cursor: "pointer",
                      }}
                    >
                      {category.name}
                    </span>
                    <button
                      type="button"
                      onClick={() =>
                        setSelectedCategories((prev) =>
                          prev.filter((cat) => cat.category.id !== category.id)
                        )
                      }
                      style={{
                        backgroundColor: "#f44336",
                        color: "white",
                        border: "none",
                        padding: "5px 10px",
                        borderRadius: "5px",
                        cursor: "pointer",
                        transition: "background-color 0.3s ease",
                      }}
                      onMouseEnter={(e) =>
                        (e.currentTarget.style.backgroundColor = "#d32f2f")
                      }
                      onMouseLeave={(e) =>
                        (e.currentTarget.style.backgroundColor = "#f44336")
                      }
                    >
                      X
                    </button>
                    {hoveredCategoryId === category.id && (
                      <div
                        style={{
                          position: "absolute",
                          backgroundColor: "#ffffff",
                          color: "#000000",
                          padding: "10px",
                          borderRadius: "5px",
                          border: "1px solid #ccc",
                          boxShadow: "0 2px 8px rgba(0, 0, 0, 0.2)",
                          zIndex: 100,
                          maxWidth: "90vw",
                          left: "50%",
                          transform: "translateX(-50%)",
                          top: "calc(100% + 5px)",
                          display: "flex",
                          flexDirection: "column",
                          gap: "1px",
                          whiteSpace: "nowrap",
                          overflow: "hidden",
                          textOverflow: "ellipsis",
                        }}
                      >
                        {subcategories.map((sub) => (
                          <div
                            key={sub.id}
                            style={{
                              fontSize: "14px",
                              whiteSpace: "nowrap",
                              overflow: "hidden",
                              textOverflow: "ellipsis",
                              display: "block",
                              margin: "5px 0",
                              color: "#555",
                            }}
                          >
                            {sub.name}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
          <div style={{ marginBottom: "20px" }}>
            <label
              style={{
                display: "block",
                fontWeight: "bold",
                marginBottom: "8px",
                color: "#333",
              }}
            >
              Severidade:
            </label>
            <select
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              required
              style={{
                width: "100%",
                padding: "8px",
                borderRadius: "4px",
                border: "1px solid #ccc",
                boxSizing: "border-box",
                marginBottom: "10px",
              }}
            >
              <option value="">Selecione a severidade</option>
              {severities.map((severity) => (
                <option key={severity.id} value={severity.id}>
                  {severity.description}
                </option>
              ))}
            </select>
          </div>
          <div
            style={{
              display: "flex",
              justifyContent: "flex-end",
              marginTop: "20px",
            }}
          >
            <button
              type="button"
              onClick={onClose}
              style={{
                backgroundColor: "#007bff",
                border: "none",
                color: "white",
                padding: "10px 20px",
                borderRadius: "5px",
                cursor: "pointer",
                transition: "background-color 0.3s ease",
                marginLeft: "10px",
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.backgroundColor = "#0056b3")
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.backgroundColor = "#007bff")
              }
            >
              Cancelar
            </button>
            <button
              type="submit"
              style={{
                backgroundColor: "#007bff",
                color: "white",
                padding: "10px 20px",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
                transition: "background-color 0.3s ease",
                marginLeft: "10px",
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.backgroundColor = "#0056b3")
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.backgroundColor = "#007bff")
              }
            >
              Criar Ticket
            </button>
          </div>
        </form>
      </div>
      {isSelectCategoryModalOpen && (
        <SelectCategoryModal
          onClose={() => setIsSelectCategoryModalOpen(false)}
          onAddCategory={handleAddCategory}
        />
      )}
    </div>
  );
};

export default CreateTicketModal;
