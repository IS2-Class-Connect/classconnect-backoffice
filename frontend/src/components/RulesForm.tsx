import { useEffect, useState } from 'react';
import api from '../api/axios';
import '../styles/Rules.css';

interface Rule {
  id: string;
  title: string;
  description: string;
  effective_date: string;
  applicable_conditions: string[];
}

interface NewRule {
  title: string;
  description: string;
  effective_date: string;
  applicable_conditions: string;
}

const RulesForm = () => {
  const [rules, setRules] = useState<Rule[]>([]);
  const [newRule, setNewRule] = useState<NewRule>({
    title: '',
    description: '',
    effective_date: '',
    applicable_conditions: '',
  });
  const [editingRuleId, setEditingRuleId] = useState<string | null>(null);

  const fetchRules = async () => {
    try {
      const response = await api.get('/admins/rules');
      if (Array.isArray(response.data)) {
        const validRules = response.data.filter(
          (rule) => rule && rule.title && rule.id
        );
        setRules(validRules);
      } else {
        setRules([]);
      }
    } catch (error) {
      console.error('Error fetching rules:', error);
    }
  };

  useEffect(() => {
    fetchRules();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setNewRule({ ...newRule, [name]: value });
  };

  const handleEdit = (rule: Rule) => {
    setEditingRuleId(rule.id);
    setNewRule({
      title: rule.title,
      description: rule.description,
      effective_date: rule.effective_date,
      applicable_conditions: rule.applicable_conditions.join(', '),
    });
  };

  const handleCancelEdit = () => {
    setEditingRuleId(null);
    setNewRule({
      title: '',
      description: '',
      effective_date: '',
      applicable_conditions: '',
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      title: newRule.title.trim(),
      description: newRule.description.trim(),
      effective_date: newRule.effective_date,
      applicable_conditions: newRule.applicable_conditions
        .split(',')
        .map((cond) => cond.trim())
        .filter((cond) => cond.length > 0),
    };

    if (!payload.title || !payload.description || !payload.effective_date) {
      alert('Please fill all required fields.');
      return;
    }

    try {
      if (editingRuleId) {
        await api.patch(`/admins/rules/${editingRuleId}`, {
          admin_name: 'admin',
          update: payload,
        });

        setRules(
          rules.map((rule) =>
            rule.id === editingRuleId ? { ...rule, ...payload } : rule
          )
        );

        setEditingRuleId(null);
      }
      else {
        const response = await api.post('/admins/rules', payload);
        if (response.data) {
          setRules([...rules, response.data]);
        } else {
          alert('Error: no se recibió la regla creada.');
        }
      }

      setNewRule({
        title: '',
        description: '',
        effective_date: '',
        applicable_conditions: '',
      });
    } catch (error) {
      console.error('Error submitting rule:', error);
      alert('Error submitting rule. Please check console for details.');
    }
  };

  return (
    <div className="user-list-container">
      <h2 className="user-list-title">Rules List</h2>
      {rules.length === 0 ? (
        <p>No rules found</p>
      ) : (
        <table className="user-list-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Description</th>
              <th>Effective Date</th>
              <th>Conditions</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {rules
              .filter((rule) => rule !== null && rule !== undefined)
              .map((rule) => (
                <tr key={rule.id}>
                  <td>{rule.title}</td>
                  <td>{rule.description}</td>
                  <td>{rule.effective_date}</td>
                  <td>{rule.applicable_conditions.join(', ')}</td>
                  <td>
                    <button className="add-rules-button" onClick={() => handleEdit(rule)}>Edit</button>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      )}

      <h2 className="user-list-title">
        {editingRuleId ? 'Edit Rule' : 'Create New Rule'}
      </h2>
      <form onSubmit={handleSubmit} className="rules-form">
        <input
          name="title"
          placeholder="Title"
          value={newRule.title}
          onChange={handleChange}
          required
        />
        <textarea
          name="description"
          placeholder="Description"
          value={newRule.description}
          onChange={handleChange}
          required
        />
        <input
          name="effective_date"
          type="date"
          value={newRule.effective_date}
          onChange={handleChange}
          required
        />
        <input
          name="applicable_conditions"
          placeholder="Conditions (comma-separated)"
          value={newRule.applicable_conditions}
          onChange={handleChange}
        />
        <div className="top-actions">
          <button className="add-rules-button" type="submit">
            {editingRuleId ? 'Update Rule' : 'Add Rule'}
          </button>
          {editingRuleId && (
            <button 
              type="button"
              className="cancel-button "
              onClick={handleCancelEdit}
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default RulesForm;
