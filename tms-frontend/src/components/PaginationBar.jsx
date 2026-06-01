import React from 'react';

export default function PaginationBar({ offset, limit, totalCount, onPrevious, onNext, isLoading }) {
  const isLeftDisabled = offset === 0 || isLoading;
  const isRightDisabled = offset + limit >= totalCount || isLoading;

  return (
    <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <button disabled={isLeftDisabled} onClick={onPrevious}>
        Previous
      </button>
      
      <span style={{ fontSize: '14px', color: '#666' }}>
        Showing {totalCount === 0 ? 0 : offset + 1} - {Math.min(offset + limit, totalCount)} of {totalCount} tasks
      </span>
      
      <button disabled={isRightDisabled} onClick={onNext}>
        Next
      </button>
    </div>
  );
}