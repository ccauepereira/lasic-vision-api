import React from 'react';

interface TagsListProps {
  tags: string[];
}

export const TagsList: React.FC<TagsListProps> = ({ tags }) => {
  return (
    <div className="tags-section">
      <h3 className="section-subtitle">🏷️ Tags Automáticas</h3>
      <div className="badges-wrapper">
        {tags.map((tag, idx) => (
          <span key={idx} className="badge-pill">
            #{tag}
          </span>
        ))}
      </div>
    </div>
  );
};
