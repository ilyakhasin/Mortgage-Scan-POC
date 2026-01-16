/**
 * Veryfi API Client for uploading documents and extracting mortgage fields
 */

const VERYFI_API_KEY = process.env.VERYFI_API_KEY || '';
const VERYFI_API_URL = 'https://api.veryfi.com/api/v7/partner/documents';

/**
 * Upload image to Veryfi and return parsed document data
 * @param {string} base64Image - Base64 encoded image data
 * @returns {Promise<Object>} - Veryfi API response
 */
export async function uploadDocument(base64Image) {
  if (!VERYFI_API_KEY) {
    throw new Error('VERYFI_API_KEY is not configured. Please set it in repository Settings → Secrets → Actions.');
  }

  try {
    const formData = new FormData();
    formData.append('file', {
      uri: `data:image/jpeg;base64,${base64Image}`,
      type: 'image/jpeg',
      name: 'mortgage_statement.jpg',
    });

    const response = await fetch(VERYFI_API_URL, {
      method: 'POST',
      headers: {
        'Authorization': `apikey ${VERYFI_API_KEY}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Veryfi API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
}

/**
 * Map Veryfi response to canonical mortgage fields
 * @param {Object} veryfiResponse - Raw Veryfi API response
 * @returns {Array<Object>} - Array of field objects with label and value
 */
export function mapFields(veryfiResponse) {
  // Extract common fields from Veryfi response
  // Note: Field locations may vary based on document format
  const {
    vendor = {},
    total = 0,
    date = '',
    due_date = '',
    line_items = [],
    custom_fields = {},
  } = veryfiResponse;

  // Helper to safely extract values
  const getValue = (obj, key, defaultValue = 'N/A') => {
    return obj && obj[key] ? obj[key] : defaultValue;
  };

  // Map to 10 canonical mortgage fields
  return [
    {
      label: 'Borrower name',
      value: getValue(custom_fields, 'borrower_name', getValue(veryfiResponse, 'bill_to_name')),
    },
    {
      label: 'Loan number',
      value: getValue(custom_fields, 'loan_number', getValue(veryfiResponse, 'invoice_number')),
    },
    {
      label: 'Property address',
      value: getValue(custom_fields, 'property_address', getValue(veryfiResponse, 'bill_to_address')),
    },
    {
      label: 'Statement date',
      value: date || 'N/A',
    },
    {
      label: 'Due date',
      value: due_date || 'N/A',
    },
    {
      label: 'Current principal balance',
      value: getValue(custom_fields, 'principal_balance', 'N/A'),
    },
    {
      label: 'Interest rate',
      value: getValue(custom_fields, 'interest_rate', 'N/A'),
    },
    {
      label: 'Monthly payment',
      value: getValue(custom_fields, 'monthly_payment', total ? `$${total.toFixed(2)}` : 'N/A'),
    },
    {
      label: 'Servicer name',
      value: getValue(vendor, 'name', getValue(veryfiResponse, 'vendor_name')),
    },
    {
      label: 'Account number',
      value: getValue(custom_fields, 'account_number', getValue(veryfiResponse, 'account_number')),
    },
  ];
}
