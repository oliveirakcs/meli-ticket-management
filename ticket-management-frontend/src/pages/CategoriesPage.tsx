import React, { useState, useEffect } from "react";
import {
  fetchCategories,
  createCategory,
  updateCategory,
  deleteCategory,
} from "../services/api";
import { Category, CategoryCreation } from "../types/generalTypes";
import CategoryModal from "../components/CategoryModal";
import SubcategoryModal from "../components/SubcategoryModal";
import {
  fetchSubcategoriesByCategory,
  createSubcategory,
  updateSubcategory,
  deleteSubcategory,
} from "../services/api";
import { Subcategory, SubcategoryCreation } from "../types/generalTypes";
import { useNavigate } from "react-router-dom";
import mercadoLivreLogo from "../icons/mercado-livre.svg";

const CategoriesPage: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [expandedCategoryIds, setExpandedCategoryIds] = useState<Set<string>>(
    new Set()
  );
  const [selectedCategory, setSelectedCategory] = useState<Category | null>(
    null
  );
  const [isCategoryModalOpen, setIsCategoryModalOpen] = useState(false);
  const [isEditCategoryMode, setIsEditCategoryMode] = useState(false);
  const [subcategories, setSubcategories] = useState<Subcategory[]>([]);
  const [selectedSubcategory, setSelectedSubcategory] =
    useState<Subcategory | null>(null);
  const [isSubcategoryModalOpen, setIsSubcategoryModalOpen] = useState(false);
  const [isEditSubcategoryMode, setIsEditSubcategoryMode] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const loadData = async () => {
      try {
        const categoriesData = await fetchCategories();
        setCategories(categoriesData);
      } catch (error) {
        console.error("Erro ao carregar dados:", error);
        alert("Erro ao carregar dados.");
      }
    };
    loadData();
  }, []);

  const loadSubcategoriesByCategory = async (categoryId: string) => {
    try {
      const subcategoriesData = await fetchSubcategoriesByCategory(categoryId);
      setSubcategories((prevSubcategories) => [
        ...prevSubcategories.filter((sub) => sub.category_id !== categoryId),
        ...subcategoriesData,
      ]);
    } catch (error) {
      console.error("Erro ao carregar subcategorias:", error);
      alert("Erro ao carregar subcategorias.");
    }
  };

  const handleCreateCategory = async (category: CategoryCreation) => {
    try {
      const newCategory = await createCategory(category);
      setCategories((prevCategories) => [...prevCategories, newCategory]);
      alert("Categoria criada com sucesso!");
    } catch (error) {
      console.error("Erro ao criar categoria:", error);
      alert("Erro ao criar categoria.");
    }
  };

  const handleUpdateCategory = async (updatedCategory: Category) => {
    try {
      await updateCategory(updatedCategory.id, updatedCategory);
      setCategories((prevCategories) =>
        prevCategories.map((category) =>
          category.id === updatedCategory.id ? updatedCategory : category
        )
      );
      alert("Categoria atualizada com sucesso!");
    } catch (error) {
      console.error("Erro ao atualizar categoria:", error);
      alert("Erro ao atualizar categoria.");
    }
  };

  const handleDeleteCategory = async (id: string) => {
    const confirmDelete = window.confirm(
      "Tem certeza que deseja deletar esta Categoria?"
    );
    if (confirmDelete) {
      try {
        await deleteCategory(id);
        setCategories((prevCategories) =>
          prevCategories.filter((category) => category.id !== id)
        );
        alert("Categoria deletada com sucesso!");
      } catch (error) {
        console.error("Erro ao deletar categoria:", error);
        alert("Erro ao deletar categoria.");
      }
    }
  };

  const handleCreateSubcategory = async (subcategory: SubcategoryCreation) => {
    try {
      const newSubcategory = await createSubcategory(subcategory);
      setSubcategories((prevSubcategories) => [
        ...prevSubcategories,
        newSubcategory,
      ]);
      alert("Subcategoria criada com sucesso!");
    } catch (error) {
      console.error("Erro ao criar subcategoria:", error);
      alert("Erro ao criar subcategoria.");
    }
  };

  const handleUpdateSubcategory = async (updatedSubcategory: Subcategory) => {
    try {
      const { category_id } = updatedSubcategory;
      await updateSubcategory(updatedSubcategory.id, updatedSubcategory);
      await loadSubcategoriesByCategory(category_id);
      alert("Subcategoria atualizada com sucesso!");
    } catch (error) {
      console.error("Erro ao atualizar subcategoria:", error);
      alert("Erro ao atualizar subcategoria.");
    }
  };

  const handleDeleteSubcategory = async (id: string) => {
    const confirmDelete = window.confirm(
      "Tem certeza que deseja deletar esta Subcategoria?"
    );
    if (confirmDelete) {
      try {
        await deleteSubcategory(id);
        setSubcategories((prevSubcategories) =>
          prevSubcategories.filter((subcategory) => subcategory.id !== id)
        );
        alert("Subcategoria deletada com sucesso!");
      } catch (error) {
        console.error("Erro ao deletar subcategoria:", error);
        alert("Erro ao deletar subcategoria.");
      }
    }
  };

  const handleEditCategoryClick = (category: Category) => {
    setSelectedCategory(category);
    setIsEditCategoryMode(true);
    setIsCategoryModalOpen(true);
  };

  const handleCreateCategoryClick = () => {
    setSelectedCategory(null);
    setIsEditCategoryMode(false);
    setIsCategoryModalOpen(true);
  };

  const handleEditSubcategoryClick = (subcategory: Subcategory) => {
    setSelectedSubcategory(subcategory);
    setIsEditSubcategoryMode(true);
    setIsSubcategoryModalOpen(true);
  };

  const handleCreateSubcategoryClick = (category_id: string) => {
    setSelectedSubcategory(null);
    setIsEditSubcategoryMode(false);
    setSelectedCategory(
      categories.find((category) => category.id === category_id) || null
    );
    setIsSubcategoryModalOpen(true);
  };

  const closeCategoryModal = () => {
    setIsCategoryModalOpen(false);
    setSelectedCategory(null);
  };

  const closeSubcategoryModal = () => {
    setIsSubcategoryModalOpen(false);
    setSelectedSubcategory(null);
  };

  const handleNavigation = (path: string) => {
    navigate(path);
    setIsMenuOpen(false);
  };

  const toggleCategoryExpansion = async (categoryId: string) => {
    setExpandedCategoryIds((prevExpandedCategoryIds) => {
      const newExpandedCategoryIds = new Set(prevExpandedCategoryIds);
      if (newExpandedCategoryIds.has(categoryId)) {
        newExpandedCategoryIds.delete(categoryId);
      } else {
        newExpandedCategoryIds.add(categoryId);
        loadSubcategoriesByCategory(categoryId);
      }
      return newExpandedCategoryIds;
    });
  };

  return (
    <div
      style={{
        maxWidth: "1200px",
        margin: "0 auto",
        padding: "20px",
      }}
    >
      <div
        style={{
          marginBottom: "20px",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
          width: "100%",
          marginTop: "10px",
        }}
      >
        <img
          src={mercadoLivreLogo}
          alt="Mercado Livre"
          style={{
            width: "150px",
            height: "auto",
          }}
        />
        <span
          style={{
            color: "#2d3277",
            fontSize: "18px",
            fontFamily: "Arial, sans-serif",
            marginTop: "10px",
            textAlign: "center",
          }}
        >
          Ticket Management App
        </span>
      </div>
      <div
        style={{
          padding: "20px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          marginTop: "20px",
          position: "relative",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            width: "100%",
          }}
        >
          <div>
            <button
              style={{
                backgroundColor: isMenuOpen ? "#0056b3" : "#007bff",
                border: "none",
                width: "60px",
                height: "50px",
                borderRadius: "5px",
                color: "white",
                cursor: "pointer",
                transition: "transform 0.3s ease, background-color 0.3s ease",
                transform: isMenuOpen ? "rotate(90deg)" : "rotate(0deg)",
                fontSize: "24px",
                boxShadow: "0 2px 4px rgba(0, 0, 0, 0.2)",
                outline: "none",
                position: "relative",
                marginBottom: "10px",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
              }}
              onClick={() => setIsMenuOpen((prev) => !prev)}
              onMouseEnter={(e) =>
                (e.currentTarget.style.backgroundColor = "#0056b3")
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.backgroundColor = isMenuOpen
                  ? "#0056b3"
                  : "#007bff")
              }
            >
              <span
                style={{
                  display: "block",
                  width: "25px",
                  height: "3px",
                  backgroundColor: "white",
                  margin: "2px auto",
                  transition: "all 0.3s",
                  transform: isMenuOpen
                    ? "rotate(-45deg) translate(-5px, 5px)"
                    : "rotate(0)",
                }}
              />
              <span
                style={{
                  display: "block",
                  width: "25px",
                  height: "3px",
                  backgroundColor: "white",
                  margin: "2px auto",
                  transition: "all 0.3s",
                  opacity: isMenuOpen ? 0 : 1,
                }}
              />
              <span
                style={{
                  display: "block",
                  width: "25px",
                  height: "3px",
                  backgroundColor: "white",
                  margin: "2px auto",
                  transition: "all 0.3s",
                  transform: isMenuOpen
                    ? "rotate(45deg) translate(-5px, -5px)"
                    : "rotate(0)",
                }}
              />
            </button>
            {isMenuOpen && (
              <div
                style={{
                  position: "absolute",
                  backgroundColor: "#007bff",
                  padding: "20px",
                  marginTop: "10px",
                  borderRadius: "8px",
                  boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
                  zIndex: 1000,
                }}
              >
                <ul style={{ listStyleType: "none", padding: 0, margin: 0 }}>
                  <li
                    style={{
                      padding: "10px",
                      marginBottom: "5px",
                      borderRadius: "4px",
                      cursor: "pointer",
                      transition: "background-color 0.3s",
                      backgroundColor: "#0056b3",
                      color: "white",
                    }}
                    onClick={() => navigate("/")}
                    onMouseEnter={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        "#004494")
                    }
                    onMouseLeave={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        "#0056b3")
                    }
                  >
                    Página Principal
                  </li>
                  <li
                    style={{
                      padding: "10px",
                      marginBottom: "5px",
                      borderRadius: "4px",
                      cursor: "pointer",
                      transition: "background-color 0.3s",
                      backgroundColor: "#0056b3",
                      color: "white",
                    }}
                    onClick={() => handleNavigation("/severities")}
                    onMouseEnter={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        "#004494")
                    }
                    onMouseLeave={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        "#0056b3")
                    }
                  >
                    Severities
                  </li>
                  <li
                    style={{
                      padding: "10px",
                      borderRadius: "4px",
                      cursor: "pointer",
                      transition: "background-color 0.3s",
                      backgroundColor: "#0056b3",
                      color: "white",
                    }}
                    onClick={() => handleNavigation("/users")}
                    onMouseEnter={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        "#004494")
                    }
                    onMouseLeave={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        "#0056b3")
                    }
                  >
                    Usuários
                  </li>
                </ul>
              </div>
            )}
          </div>
          <div
            style={{
              flex: 1,
            }}
          ></div>
        </div>
        <h1 style={{ color: "#333", textAlign: "center" }}>Categorias</h1>

        <button
          onClick={handleCreateCategoryClick}
          style={{
            backgroundColor: "#007bff",
            color: "white",
            padding: "10px 20px",
            borderRadius: "5px",
            border: "none",
            cursor: "pointer",
            marginBottom: "20px",
            display: "block",
            marginLeft: "auto",
            transition: "background-color 0.3s ease",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.backgroundColor = "#0056b3")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.backgroundColor = "#007bff")
          }
        >
          Criar Categoria
        </button>

        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)",
            marginTop: "20px",
          }}
        >
          <thead>
            <tr
              style={{
                backgroundColor: "#f4f4f4",
                color: "#333",
              }}
            >
              <th style={{ padding: "10px", borderBottom: "2px solid #ddd" }}>
                Nome da Categoria
              </th>
              <th style={{ padding: "10px", borderBottom: "2px solid #ddd" }}>
                Ações
              </th>
            </tr>
          </thead>
          <tbody>
            {categories.map((category) => (
              <React.Fragment key={category.id}>
                <tr
                  style={{
                    backgroundColor: "#fff",
                    borderBottom: "1px solid #ddd",
                    cursor: "pointer",
                  }}
                  onClick={() => toggleCategoryExpansion(category.id)}
                >
                  <td style={{ padding: "10px", textAlign: "center" }}>
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                    >
                      <span
                        style={{
                          display: "inline-block",
                          width: "0",
                          height: "0",
                          borderLeft: "6px solid transparent",
                          borderRight: "6px solid transparent",
                          borderTop: expandedCategoryIds.has(category.id)
                            ? "none"
                            : "6px solid #333",
                          borderBottom: expandedCategoryIds.has(category.id)
                            ? "6px solid #333"
                            : "none",
                          transition: "transform 0.3s ease",
                          transform: expandedCategoryIds.has(category.id)
                            ? "rotate(180deg)"
                            : "rotate(180deg)",
                          marginRight: "10px",
                        }}
                      ></span>
                      {category.name}
                    </div>
                  </td>
                  <td style={{ padding: "10px", textAlign: "center" }}>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEditCategoryClick(category);
                      }}
                      style={{
                        backgroundColor: "#ffc107",
                        color: "#333",
                        padding: "5px 10px",
                        borderRadius: "5px",
                        border: "none",
                        cursor: "pointer",
                        marginRight: "5px",
                        transition: "background-color 0.3s ease",
                      }}
                      onMouseEnter={(e) =>
                        (e.currentTarget.style.backgroundColor = "#e0a800")
                      }
                      onMouseLeave={(e) =>
                        (e.currentTarget.style.backgroundColor = "#ffc107")
                      }
                    >
                      Editar
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteCategory(category.id);
                      }}
                      style={{
                        backgroundColor: "#dc3545",
                        color: "white",
                        padding: "5px 10px",
                        borderRadius: "5px",
                        border: "none",
                        cursor: "pointer",
                        transition: "background-color 0.3s ease",
                      }}
                      onMouseEnter={(e) =>
                        (e.currentTarget.style.backgroundColor = "#c82333")
                      }
                      onMouseLeave={(e) =>
                        (e.currentTarget.style.backgroundColor = "#dc3545")
                      }
                    >
                      Deletar
                    </button>
                  </td>
                </tr>
                {expandedCategoryIds.has(category.id) && (
                  <tr
                    style={{
                      backgroundColor: "#f9f9f9",
                      borderBottom: "1px solid #ddd",
                    }}
                  >
                    <td
                      colSpan={2}
                      style={{ padding: "10px", textAlign: "center" }}
                    >
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "center",
                          alignItems: "center",
                          flexDirection: "column",
                        }}
                      >
                        <ul
                          style={{
                            padding: 0,
                            listStyleType: "none",
                            textAlign: "center",
                          }}
                        >
                          {subcategories
                            .filter(
                              (subcategory) =>
                                subcategory.category_id === category.id
                            )
                            .map((subcategory) => (
                              <li
                                key={subcategory.id}
                                style={{
                                  marginBottom: "5px",
                                  textAlign: "center",
                                }}
                              >
                                {subcategory.name}
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleEditSubcategoryClick(subcategory);
                                  }}
                                  style={{
                                    backgroundColor: "#ffc107",
                                    color: "#333",
                                    padding: "2px 5px",
                                    borderRadius: "3px",
                                    border: "none",
                                    cursor: "pointer",
                                    marginLeft: "5px",
                                    transition: "background-color 0.3s ease",
                                  }}
                                  onMouseEnter={(e) =>
                                    (e.currentTarget.style.backgroundColor =
                                      "#e0a800")
                                  }
                                  onMouseLeave={(e) =>
                                    (e.currentTarget.style.backgroundColor =
                                      "#ffc107")
                                  }
                                >
                                  Editar
                                </button>
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleDeleteSubcategory(subcategory.id);
                                  }}
                                  style={{
                                    backgroundColor: "#dc3545",
                                    color: "white",
                                    padding: "2px 5px",
                                    borderRadius: "3px",
                                    border: "none",
                                    cursor: "pointer",
                                    marginLeft: "5px",
                                    transition: "background-color 0.3s ease",
                                  }}
                                  onMouseEnter={(e) =>
                                    (e.currentTarget.style.backgroundColor =
                                      "#c82333")
                                  }
                                  onMouseLeave={(e) =>
                                    (e.currentTarget.style.backgroundColor =
                                      "#dc3545")
                                  }
                                >
                                  Deletar
                                </button>
                              </li>
                            ))}
                        </ul>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleCreateSubcategoryClick(category.id);
                          }}
                          style={{
                            backgroundColor: "#007bff",
                            color: "white",
                            padding: "5px 10px",
                            borderRadius: "5px",
                            border: "none",
                            cursor: "pointer",
                            marginTop: "10px",
                            transition: "background-color 0.3s ease",
                          }}
                          onMouseEnter={(e) =>
                            (e.currentTarget.style.backgroundColor = "#0056b3")
                          }
                          onMouseLeave={(e) =>
                            (e.currentTarget.style.backgroundColor = "#007bff")
                          }
                        >
                          Criar Subcategoria
                        </button>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>

        {isCategoryModalOpen && (
          <CategoryModal
            category={selectedCategory}
            isEditMode={isEditCategoryMode}
            onClose={closeCategoryModal}
            onSubmit={(category) => {
              if (isEditCategoryMode) {
                handleUpdateCategory(category as Category);
              } else {
                handleCreateCategory(category as CategoryCreation);
              }
            }}
          />
        )}

        {isSubcategoryModalOpen && (
          <SubcategoryModal
            subcategory={selectedSubcategory}
            isEditMode={isEditSubcategoryMode}
            onClose={closeSubcategoryModal}
            category_id={selectedCategory?.id || ""}
            onSubmit={(subcategory) => {
              if (isEditSubcategoryMode) {
                handleUpdateSubcategory(subcategory as Subcategory);
              } else {
                handleCreateSubcategory(subcategory as SubcategoryCreation);
              }
            }}
          />
        )}
      </div>
    </div>
  );
};

export default CategoriesPage;
