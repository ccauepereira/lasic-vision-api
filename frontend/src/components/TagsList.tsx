import React from 'react';

interface TagsListProps {
  tags: string[];
}

export const TagsList: React.FC<TagsListProps> = ({ tags }) => {
  return (
    <section className="tags-section" id="tags-section">
      <h2 className="section-title">
        <span className="icon">🏷️</span> Tags Automáticas Geradas
      </h2>

      {tags && tags.length > 0 ? (
        <div className="tags-container" id="tags-list">
          {tags.map((tag, index) => (
            <span key={index} className="tag-pill" id={`tag-${index}`}>
              #{tag}
            </span>
          ))}
        </div>
      ) : (
        <p className="no-tags">Nenhuma tag foi gerada para esta imagem.</p>
      )}
    </section>
  );
};
