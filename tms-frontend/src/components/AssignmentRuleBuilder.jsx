import React, { useState, useEffect } from 'react';

function AssignmentRuleBuilder({ rules, setRules }) {
  const [jsonText, setJsonText] = useState(JSON.stringify(rules, null, 2));
  const [error, setError] = useState(null);

  // Sync text area with external prop changes (e.g., if rules are cleared)
  useEffect(() => {
    setJsonText(JSON.stringify(rules, null, 2));
  }, [rules]);

  const handleChange = (e) => {
    const value = e.target.value;
    setJsonText(value);

    try {
      const parsed = JSON.parse(value);
      setRules(parsed);
      setError(null); // Clear error on successful parse
    } catch (err) {
      setError("Invalid JSON format");
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      <label style={{ fontWeight: 'bold' }}>Assignment Rules (JSON):</label>
      <textarea
        value={jsonText}
        onChange={handleChange}
        rows={8}
        style={{
          width: '100%',
          fontFamily: 'monospace',
          padding: '10px',
          borderColor: error ? 'red' : '#ccc',
          borderRadius: '4px'
        }}
      />
      {error && <span style={{ color: 'red', fontSize: '12px' }}>{error}</span>}
      <small style={{ color: '#666' }}>Format: [ {"{"} "field": "dept", "operator": "EQUALS", "value": "Design" {"}"} ]</small>
    </div>
  );
}

export default AssignmentRuleBuilder;