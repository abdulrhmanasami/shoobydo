# Data Dictionary (Draft)

This draft maps discovered column names to proposed unified keys.

## Unified Columns (Proposed)
- supplier_name: Supplier_Name, "اسم المورد", Recommended_Suppliers → supplier_name
- monthly_cost_eur: Monthly_Cost_EUR, Monthly_Fee_EUR, "الرسوم الشهرية (يورو)", "التكلفة الشهرية (يورو)" → monthly_cost_eur
- monthly_margin_eur: Monthly_Margin_EUR, Gross_Margin_EUR → monthly_margin_eur
- commission_percentage: Commission_Fee, "Commission (%)" → commission_percentage
- minimum_order_qty: Min_Order_Qty, "الحد الأدنى للطلب" → minimum_order_qty
- country_region: Country_Region, "البلد/المنطقة" → country_region
- specialization: Specialization, "التخصص" → specialization
- shipping_time_days: Shipping_Time_Days, "وقت الشحن (أيام)" → shipping_time_days
- product_price_range_eur: Product_Price_Range_EUR, "نطاق الأسعار (يورو)" → product_price_range_eur
- overall_rating: Overall_Rating, "التقييم العام" → overall_rating

> Note: Arabic labels are mapped by meaning; future ETL will normalize localized headers to these unified keys.

## api_integration
- occurrences: 4
  - suppliers_model_04.xlsx :: Complete_Comparison :: "API_Integration"
  - suppliers_model_04.xlsx :: For_Beginners :: "API_Integration"
  - suppliers_model_04.xlsx :: Premium_Suppliers :: "API_Integration"
  - suppliers_model_04.xlsx :: Local_European :: "API_Integration"

## country_region
- occurrences: 4
  - suppliers_model_04.xlsx :: Complete_Comparison :: "Country_Region"
  - suppliers_model_04.xlsx :: For_Beginners :: "Country_Region"
  - suppliers_model_04.xlsx :: Premium_Suppliers :: "Country_Region"
  - suppliers_model_04.xlsx :: Local_European :: "Country_Region"

## custom_branding
- occurrences: 4
  - suppliers_model_04.xlsx :: Complete_Comparison :: "Custom_Branding"
  - suppliers_model_04.xlsx :: For_Beginners :: "Custom_Branding"
  - suppliers_model_04.xlsx :: Premium_Suppliers :: "Custom_Branding"
  - suppliers_model_04.xlsx :: Local_European :: "Custom_Branding"

## eu_warehouses
- occurrences: 4
  - suppliers_model_04.xlsx :: Complete_Comparison :: "EU_Warehouses"
  - suppliers_model_04.xlsx :: For_Beginners :: "EU_Warehouses"
  - suppliers_model_04.xlsx :: Premium_Suppliers :: "EU_Warehouses"
  - suppliers_model_04.xlsx :: Local_European :: "EU_Warehouses"

## monthly_fee_eur
- occurrences: 4
  - suppliers_model_04.xlsx :: Complete_Comparison :: "Monthly_Fee_EUR"
  - suppliers_model_04.xlsx :: For_Beginners :: "Monthly_Fee_EUR"
  - suppliers_model_04.xlsx :: Premium_Suppliers :: "Monthly_Fee_EUR"
  - suppliers_model_04.xlsx :: Local_European :: "Monthly_Fee_EUR"

## overall_rating
- occurrences: 4
  - suppliers_model_04.xlsx :: Complete_Comparison :: "Overall_Rating"
  - suppliers_model_04.xlsx :: For_Beginners :: "Overall_Rating"
  - suppliers_model_04.xlsx :: Premium_Suppliers :: "Overall_Rating"
  - suppliers_model_04.xlsx :: Local_European :: "Overall_Rating"

## product_price_range_eur
- occurrences: 4
  - suppliers_model_04.xlsx :: Complete_Comparison :: "Product_Price_Range_EUR"
  - suppliers_model_04.xlsx :: For_Beginners :: "Product_Price_Range_EUR"
  - suppliers_model_04.xlsx :: Premium_Suppliers :: "Product_Price_Range_EUR"
  - suppliers_model_04.xlsx :: Local_European :: "Product_Price_Range_EUR"

## shipping_time_days
- occurrences: 4
  - suppliers_model_04.xlsx :: Complete_Comparison :: "Shipping_Time_Days"
  - suppliers_model_04.xlsx :: For_Beginners :: "Shipping_Time_Days"
  - suppliers_model_04.xlsx :: Premium_Suppliers :: "Shipping_Time_Days"
  - suppliers_model_04.xlsx :: Local_European :: "Shipping_Time_Days"

## specialization
- occurrences: 4
  - suppliers_model_04.xlsx :: Complete_Comparison :: "Specialization"
  - suppliers_model_04.xlsx :: For_Beginners :: "Specialization"
  - suppliers_model_04.xlsx :: Premium_Suppliers :: "Specialization"
  - suppliers_model_04.xlsx :: Local_European :: "Specialization"

## supplier_name
- occurrences: 4
  - suppliers_model_04.xlsx :: Complete_Comparison :: "Supplier_Name"
  - suppliers_model_04.xlsx :: For_Beginners :: "Supplier_Name"
  - suppliers_model_04.xlsx :: Premium_Suppliers :: "Supplier_Name"
  - suppliers_model_04.xlsx :: Local_European :: "Supplier_Name"

## advantages
- occurrences: 1
  - suppliers_model_02.xlsx :: Sheet1 :: "Advantages"

## business_model
- occurrences: 1
  - suppliers_model_02.xlsx :: Sheet1 :: "Business_Model"

## challenges
- occurrences: 1
  - suppliers_model_02.xlsx :: Sheet1 :: "Challenges"

## monthly_cost_eur
- occurrences: 1
  - suppliers_model_02.xlsx :: Sheet1 :: "Monthly_Cost_EUR"

## recommended_suppliers
- occurrences: 1
  - suppliers_model_02.xlsx :: Sheet1 :: "Recommended_Suppliers"

## unnamed_1
- occurrences: 1
  - suppliers_model_03.xlsx :: KPI Dashboard :: "Unnamed: 1"

## unnamed_2
- occurrences: 1
  - suppliers_model_03.xlsx :: KPI Dashboard :: "Unnamed: 2"

## unnamed_3
- occurrences: 1
  - suppliers_model_03.xlsx :: KPI Dashboard :: "Unnamed: 3"

## unnamed_4
- occurrences: 1
  - suppliers_model_03.xlsx :: KPI Dashboard :: "Unnamed: 4"

