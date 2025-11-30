-- Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    language VARCHAR(2) DEFAULT 'ru',
    is_blocked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Orders table
CREATE TYPE order_status AS ENUM (
    'PENDING',           -- Ожидает оплаты
    'PAID_USER',         -- Оплачен пользователем (требует проверки)
    'COMPLETED',         -- Успешно выполнен
    'REJECTED'           -- Отменен/Не успешен
);

CREATE TYPE payment_method AS ENUM (
    'USDT_TRC20',
    'USDT_BEP20',
    'BYBIT_UID',
    'CARD',
    'LOLZ'
);

CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
    service_name VARCHAR(500) NOT NULL,
    base_amount DECIMAL(10, 2) NOT NULL,        -- Базовая сумма в USD
    commission_rate DECIMAL(5, 2) NOT NULL,     -- Процент комиссии
    commission_amount DECIMAL(10, 2) NOT NULL,  -- Сумма комиссии в USD
    total_amount DECIMAL(10, 2) NOT NULL,       -- Итоговая сумма в USD
    payment_method payment_method NOT NULL,
    payment_amount DECIMAL(10, 2) NOT NULL,     -- Сумма к оплате (может быть в RUB или USD)
    payment_currency VARCHAR(10) NOT NULL,      -- USD, RUB, USDT
    status order_status DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT NOW(),
    paid_at TIMESTAMP,
    completed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Settings table (for payment details and custom texts)
CREATE TABLE IF NOT EXISTS settings (
    key VARCHAR(255) PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Initialize default settings
INSERT INTO settings (key, value) VALUES
    ('usdt_trc20_address', ''),
    ('usdt_bep20_address', ''),
    ('bybit_uid', ''),
    ('card_number', ''),
    ('lolz_requisites', ''),
    ('instruction_text_ru', 'Спасибо за оплату! Ваш заказ обрабатывается.'),
    ('instruction_text_en', 'Thank you for payment! Your order is being processed.'),
    ('info_channel_url', ''),
    ('info_support_url', ''),
    ('info_terms_url', ''),
    ('info_refund_url', '')
ON CONFLICT (key) DO NOTHING;

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_settings_updated_at BEFORE UPDATE ON settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
