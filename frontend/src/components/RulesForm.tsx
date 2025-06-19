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

  const fetchRules = async () => {
    try {
      const response = await api.get('/admins/rules');
      setRules(response.data);
    } catch (error) {
      console.error('Error fetching rules:', error);
    }
  };

  useEffect(() => {
    fetchRules();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setNewRule({ ...newRule, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        ...newRule,
        applicable_conditions: newRule.applicable_conditions
          .split(',')
          .map((cond) => cond.trim()),
      };
      const response = await api.post('/admins/rules', payload);
      setRules([...rules, response.data]);
      setNewRule({
        title: '',
        description: '',
        effective_date: '',
        applicable_conditions: '',
      });
    } catch (error) {
      console.error('Error creating rule:', error);
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
            </tr>
          </thead>
          <tbody>
            {rules.map((rule) => (
              <tr key={rule.id}>
                <td>{rule.title}</td>
                <td>{rule.description}</td>
                <td>{rule.effective_date}</td>
                <td>{rule.applicable_conditions.join(', ')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
 <h2 className="user-list-title">Create New Rule</h2>
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
          required
        />
        <div className="top-actions">
          <button className="add-rules-button" type="submit">Add Rule</button>
        </div>
      </form>
    </div>
  );
};

export default RulesForm;

